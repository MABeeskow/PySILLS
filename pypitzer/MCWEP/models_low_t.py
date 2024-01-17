# -*- coding: utf-8 -*-
# Author: Yiping Liu
# Description: This script calculates the average of a list of numbers.
# Version: 1.0
# Last Modified: May 7, 2023

import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
from scipy.optimize import minimize
from database.solid_data import solids

import public.low_level as ll

import Pitzer.methods as pm
from public.icemelting import (clegg_and_brimblecombe, spencer, monnin)

from methods import get_charge_number
from scipy.optimize import root
from functools import lru_cache, wraps
from MCWEP.methods import calculate_molality

class FluidPitzer:
    def __init__(self, x0, species, t=25, database='spencer', neutral=False, solids=None):
        """
        Initiate the solution.
        :param x0: initiate values of x(x1, x2), namely value of mNa and mCl.
        :param species: define species of a solution.
        :param t: melting temperature.
        :param database: which database to use.
        :param solids: define which solid(s) to be used for building solubility equilibrium.
        """
        self.x0 = x0
        self.t = t + 273.16
        self.species = species
        self.database = database
        self.solids = solids
        self.neutral = neutral  # to determine if a neutral species is considered in this fluid.

    def get_molalities(self, x):

        # x1: molality of Na
        # x2: molality of Cl
        x_v = tuple(x)

        molalities = calculate_molality(x_v, self.species)
        # print(molalities)
        return molalities

    def charge_balance(self, x):
        x = tuple(x)
        balance = pm.calculate_charge_balance(x, self.get_molalities(x))
        return balance

    def get_ionic_strength(self, x):
        """
        For calculating ionic strength, can be molality based or mole fraction based.
        :param x: a tuple (x1,x2).
        :return: ionic strength.
        """

        i = pm.calculate_ionic_strength(self.get_molalities(x))
        return i

    def get_z(self, x):
        molalities = self.get_molalities(x)
        ions = molalities.keys()
        z_value = 0
        for ion in ions:
            charge_number = pm.get_charge_number(ion)
            z_value += molalities[ion] * abs(charge_number)
        return z_value

    def get_component_groups(self, x):
        components = tuple(self.get_molalities(x).keys())
        groups = pm.group_components(components)
        return groups

    def get_a_phi(self):
        return pm.a_phi_spencer(self.t)

    def get_b(self, x):
        pair_parameters = {}
        cation_anion_pairs = self.get_component_groups(x)['cation_anion_pairs']
        for cap in cation_anion_pairs:
            pair_parameters[cap] = pm.beta_calculate(
                ion_pair=cap,
                ionic_strength=self.get_ionic_strength(x),
                t=self.t,
                database=self.database
            )
        return pair_parameters

    def get_b_phi(self, x):
        pair_parameters = {}
        cation_anion_pairs = self.get_component_groups(x)['cation_anion_pairs']
        for cap in cation_anion_pairs:
            pair_parameters[cap] = pm.beta_phi_calculate(
                ion_pair=cap,
                ionic_strength=self.get_ionic_strength(x),
                t=self.t,
                database=self.database
            )

        return pair_parameters

    def get_b_prime(self, x):

        """
        Get Betas ready for calculating the "F" function.
        :return: betas for each type of salt
        """

        pair_parameters = {}
        cation_anion_pairs = self.get_component_groups(x)['cation_anion_pairs']

        for cap in cation_anion_pairs:
            pair_parameters[cap] = pm.beta_prime_calculate(
                ion_pair=cap,
                ionic_strength=self.get_ionic_strength(x),
                t=self.t,
                database=self.database
            )
        return pair_parameters

    def get_c(self, c):
        pair_parameters = {}
        cation_anion_pairs = self.get_component_groups(c)['cation_anion_pairs']
        for cap in cation_anion_pairs:
            pair_parameters[cap] = pm.c_calculate(
                ion_pair=cap,
                t=self.t,
                database=self.database
            )
        return pair_parameters

    def get_cc_phi(self, x):
        cation_pairs = self.get_component_groups(x)['cation_pairs']
        phi_dict = {}
        for cation_pair in cation_pairs:
            phi_dict[cation_pair] = pm.cc_phi_calculate(
                ion_pair=cation_pair,
                ionic_strength=self.get_ionic_strength(x),
                a_phi=self.get_a_phi(),
                t=self.t,
                database=self.database
            )
        return phi_dict

    def get_cc_phi_prime_phi(self, x):
        i = self.get_ionic_strength(x)
        dict = {}
        phis = self.get_cc_phi(x)

        for pair in phis.keys():
            dict[pair] = phis[pair]["phi"] + i * phis[pair]["phi_prime"]
        return dict

    def get_aa_phi(self, x):
        if self.get_component_groups(x)['anion_pairs']:
            anion_pairs = self.get_component_groups(x)['anion_pairs']
            phi_dict = {}
            for anion_pair in anion_pairs:
                phi_dict[anion_pair] = pm.aa_phi_calculate(
                    ion_pair=anion_pair,
                    ionic_strength=self.get_ionic_strength(x),
                    a_phi=self.get_a_phi(),
                    t=self.t,
                    database=self.database
                )
            return phi_dict
        return 'Anions less than 1'

    def get_aa_phi_prime_phi(self, x):
        if self.get_component_groups(x)['anion_pairs']:
            i = self.get_ionic_strength(x)
            phi_prime_phi_dict = {}
            phis = self.get_aa_phi(x)
            for pair in phis.keys():
                phi_prime_phi_dict[pair] = phis[pair]["phi"] + i * phis[pair]["phi_prime"]
            return phi_prime_phi_dict

    def get_cca_psi(self, x):
        cation_pairs = self.get_component_groups(x)['cation_pairs']
        anions = self.get_component_groups(x)['anions']
        cca_pairs = {}
        for cation_pair in cation_pairs:
            cation1 = cation_pair[0]
            cation2 = cation_pair[1]
            for anion in anions:
                rd = pm.ternary_parameters_ready((cation1, cation2, anion), self.t, dbname=self.database)
                cca_pairs[cation1, cation2, anion] = pm.get_parameter(pair=(cation1, cation2, anion), name='psi',
                                                                      data=rd, t=self.t)
        return cca_pairs

    def get_aac_psi(self, x):
        if self.get_component_groups(x)['anion_pairs']:
            anion_pairs = self.get_component_groups(x)['anion_pairs']
            cations = self.get_component_groups(x)['cations']
            aac_pairs = {}
            for anion_pair in anion_pairs:
                anion_list = list(anion_pair)
                anion1 = anion_list[0]
                anion2 = anion_list[1]
                for cation in cations:
                    rd = pm.ternary_parameters_ready((anion1, anion2, cation), self.t, database=self.database)
                    aac_pairs[anion1, anion2, cation] = pm.get_parameter(pair=(anion1, anion2, cation), name='psi',
                                                                         data=rd, t=self.t)
            return aac_pairs

    def get_lambdas(self, x):
        neutral_ion_pairs = self.get_component_groups(x)['neutral_ion_pairs']
        lambdas = {}
        for pair in neutral_ion_pairs:
            rd = pm.binary_parameters_ready(pair=pair, t=self.t,  dbname = self.database)
            lambda_value = pm.get_parameter(pair=pair, name='lambda', data=rd, t=self.t)
            lambdas[pair] = lambda_value
        return lambdas

    def get_zetas(self, x):
        nca_pairs = self.get_component_groups(x)['neutral_cation_anion_pairs']
        zetas = {}
        for pair in nca_pairs:
            rd = pm.ternary_parameters_ready(pair=pair, t=self.t, database=self.database)
            zeta_value = pm.get_parameter(pair=pair, name='zeta', data=rd, t=self.t)
            zetas[pair] = zeta_value
        return zetas

    def get_osmotic_coefficient(self, x):
        groups = self.get_component_groups(x)
        molalities = self.get_molalities(x)
        m_sum = sum(molalities.values())
        i = self.get_ionic_strength(x)
        a_phi = self.get_a_phi()
        z = self.get_z(x)
        b = self.get_b_phi(x)
        c = self.get_c(x)
        cations = groups['cations']
        cation_pairs = groups['cation_pairs']
        anions = groups['anions']
        anion_pairs = groups['anion_pairs']
        cc_phis = self.get_cc_phi_prime_phi(x)
        cca_psis = self.get_cca_psi(x)

        neutrals = groups['neutrals']
        lambdas = self.get_lambdas(x)
        zetas = self.get_zetas(x)
        nca_pairs = groups['neutral_cation_anion_pairs']

        item0 = (2 / m_sum)

        item1 = -(a_phi * i ** 1.5) / (1 + 1.2 * i ** 0.5)

        item2 = 0
        for cap in b.keys():
            m_1 = molalities[cap[0]]
            m_2 = molalities[cap[1]]

            b_phi = 0
            for key in b.keys():
                if set(cap) == set(key):
                    b_phi = b[key]

            c_value = 0
            for key in c.keys():
                if set(cap) == set(key):
                    c_value = c[key]

            item2 += m_1 * m_2 * (b_phi + z * c_value)

        item3 = 0
        for cp in cation_pairs:
            c1 = cp[0]
            c2 = cp[1]

            m_c1 = molalities[c1]
            m_c2 = molalities[c2]

            # find value of cc_phi
            cc_phi = 0
            for key in cc_phis.keys():
                if {cp[0], cp[1]} == set(key):
                    cc_phi = cc_phis[key]

            item3_subitem1 = 0
            for anion in anions:
                m_a = molalities[anion]

                # find value of cca_psi
                cca_psi = 0
                for key in cca_psis.keys():
                    if set(key) == {c1, c2, anion}:
                        cca_psi = cca_psis[key]

                item3_subitem1 += m_a * cca_psi

            item3 += m_c1 * m_c2 * (cc_phi + item3_subitem1)

        item4 = 0

        if len(anions) > 1:
            aa_phis = self.get_aa_phi_prime_phi(x)
            aac_psis = self.get_aac_psi(x)

            for ap in anion_pairs:
                m_a1 = molalities[ap[0]]
                m_a2 = molalities[ap[1]]

                # find value of aa_phi
                aa_phi = 0
                for key in aa_phis.keys():
                    if {ap[0], ap[1]} == set(key):
                        aa_phi = aa_phis[key]

                item4_subitem1 = 0
                for cation in cations:
                    m_c = molalities[cation]

                    aac_psi = 0

                    # find value of aac_psi
                    for key in cca_psis.keys():
                        if {ap[0], ap[1], cation} == set(key):
                            aac_psi = aac_psis[key]

                    item4_subitem1 += m_c * aac_psi
                item4 += m_a1 * m_a2 * (aa_phi + item4_subitem1)

        item5 = 0
        for neutral in neutrals:
            m_n = molalities[neutral]
            for cation in cations:
                m_c = molalities[cation]

                lambda_nc = 0
                for key in lambdas.keys():
                    if {neutral, cation} == set(key):
                        lambda_nc = lambdas[key]
                item5 += m_n * m_c * lambda_nc

        item6 = 0
        for neutral in neutrals:
            m_n = molalities[neutral]
            for anion in anions:
                m_a = molalities[anion]

                lambda_na = 0
                for key in lambdas.keys():
                    if {neutral, anion} == set(key):
                        lambda_na = lambdas[key]
                item6 += m_n * m_a * lambda_na

        item7 = 0
        for nca_pair in nca_pairs:
            m1 = molalities[nca_pair[0]]
            m2 = molalities[nca_pair[1]]
            m3 = molalities[nca_pair[2]]

            zeta_nca = 0
            for key in zetas.keys():
                if set(nca_pair) == set(key):
                    zeta_nca = zetas[key]

            item7 += m1 * m2 * m3 * zeta_nca

        osmotic_coefficient = item0 * (item1 + item2 + item3 + item4 + item5 + item6 + item7) + 1
        return osmotic_coefficient

    def get_water_activity(self, x):
        m_sum = sum(self.get_molalities(x).values())
        phi = self.get_osmotic_coefficient(x)
        ln_activity = -phi * m_sum / 55.50844
        return ln_activity

    def get_f_uppercase(self, x):
        a_phi = self.get_a_phi()
        i = self.get_ionic_strength(x)
        component_groups = self.get_component_groups(x)
        cation_pairs = component_groups['cation_pairs']
        anion_pairs = component_groups['anion_pairs']
        molalities = self.get_molalities(x)
        ca_beta_primes = self.get_b_prime(x)
        cation_anion_pairs = component_groups['cation_anion_pairs']
        cc_phis = self.get_cc_phi(x)
        aa_phis = self.get_aa_phi(x)
        f_gamma = pm.get_f_gamma(a_phi, i)

        item0 = f_gamma

        item1 = 0
        for cap in cation_anion_pairs:
            m_p1 = molalities[cap[0]]
            m_p2 = molalities[cap[1]]
            ca_beta_prime = 0

            # find the value of beta_prime of cap
            for key in ca_beta_primes.keys():
                if {cap[0], cap[1]} == set(key):
                    ca_beta_prime = ca_beta_primes[key]

            item1 += m_p1 * m_p2 * ca_beta_prime

        item2 = 0
        for cp in cation_pairs:
            m_p1 = molalities[cp[0]]
            m_p2 = molalities[cp[1]]

            cc_phi_prime = 0

            # find the value of beta_prime of cap
            for key in cc_phis.keys():
                if {cp[0], cp[1]} == set(key):
                    cc_phi_prime = cc_phis[key]['phi_prime']

            item2 += m_p1 * m_p2 * cc_phi_prime

        item3 = 0
        if anion_pairs:
            for ap in anion_pairs:
                m_a1 = molalities[ap[0]]
                m_a2 = molalities[ap[1]]

                aa_phi_prime = 0
                for key in aa_phis.keys():
                    if {ap[0], ap[1]} == set(key):
                        aa_phi_prime = aa_phis[key]['phi_prime']
                item3 += m_a1 * m_a2 * aa_phi_prime

        f_uppercase = item0 + item1 + item2 + item3
        return f_uppercase

    def get_cation_activity_coefficients(self, target_cation, x):
        groups = self.get_component_groups(x)
        cations = groups['cations']
        anions = groups['anions']
        anion_pairs = groups['anion_pairs']
        cation_anion_pairs = groups['cation_anion_pairs']
        neutrals = groups['neutrals']
        molalities = self.get_molalities(x)
        target_cation = target_cation
        betas = self.get_b(x)
        cs = self.get_c(x)
        z = self.get_z(x)
        lambdas = self.get_lambdas(x)
        zetas = self.get_zetas(x)
        cc_phis = self.get_cc_phi(x)
        cation_psis = self.get_cca_psi(x)
        anion_psis = self.get_aac_psi(x)

        f_uppercase = self.get_f_uppercase(x)
        charge_number = get_charge_number(target_cation)

        item0 = charge_number ** 2 * f_uppercase

        item1 = 0
        for anion in anions:
            m_a = molalities[anion]
            beta_ca = 0
            for key in betas.keys():
                if {target_cation, anion} == set(key):
                    beta_ca = betas[key]
            c_ca = 0
            for key in cs.keys():
                if {target_cation, anion} == set(key):
                    c_ca = cs[key]
            item1 += m_a * (2 * beta_ca + z * c_ca)

        item2 = 0
        for cation in cations:
            if cation != target_cation:
                m_c = molalities[cation]
                phi_mc = 0
                for key in cc_phis.keys():
                    if set(key) == {cation, target_cation}:
                        phi_mc = cc_phis[key]['phi']

                item2_subitem1 = 0
                for anion in anions:
                    m_a = molalities[anion]
                    for tkey in cation_psis.keys():
                        if {target_cation, cation, anion} == set(tkey):
                            item2_subitem1 += m_a * cation_psis[tkey]
                item2 += m_c * (2 * phi_mc + item2_subitem1)

        item3 = 0
        if anion_pairs:
            for ap in anion_pairs:
                m_a1 = molalities[ap[0]]
                m_a2 = molalities[ap[1]]
                psi_maa = 0

                # find match for psi
                for key in anion_psis.keys():
                    if {ap[0], ap[1], target_cation} == set(key):
                        psi_maa = anion_psis[key]

                item3 += m_a1 * m_a2 * psi_maa

        item4 = 0
        for cap in cation_anion_pairs:
            ion1 = cap[0]
            ion2 = cap[1]
            c_ca = 0

            # find match for c_ca
            for key in cs.keys():
                if set(key) == {ion1, ion2}:
                    c_ca = cs[key]

            item4 += molalities[ion1] * molalities[ion2] * c_ca

        item5 = 0
        for neutral in neutrals:
            m_n = molalities[neutral]

            lambda_nm = 0
            for key in lambdas.keys():
                if {neutral, target_cation} == set(key):
                    lambda_nm = lambdas[key]
            item5 += m_n * lambda_nm

        item6 = 0
        for neutral in neutrals:
            m_n = molalities[neutral]
            for anion in anions:
                m_a = molalities[anion]

                zeta_nam = 0
                for key in zetas.keys():
                    if {target_cation, anion, neutral} == set(key):
                        zeta_nam = zetas[key]
                item6 += m_n * m_a * zeta_nam

        ln_coefficient = item0 + item1 + item2 + item3 + abs(charge_number) * item4 + 2 * item5 + item6
        return ln_coefficient

    def get_anion_activity_coefficients(self, target_anion, x):
        groups = self.get_component_groups(x)
        cations = groups['cations']
        anions = groups['anions']
        cation_pairs = groups['cation_pairs']
        cation_anion_pairs = groups['cation_anion_pairs']
        neutrals = groups['neutrals']
        lambdas = self.get_lambdas(x)
        zetas = self.get_zetas(x)
        molalities = self.get_molalities(x)
        target_anion = target_anion
        betas = self.get_b(x)
        cs = self.get_c(x)
        z = self.get_z(x)

        aa_phis = self.get_aa_phi(x)

        aac_psis = self.get_aac_psi(x)
        cca_psis = self.get_cca_psi(x)

        f_uppercase = self.get_f_uppercase(x)
        charge_number = get_charge_number(target_anion)

        item0 = charge_number ** 2 * f_uppercase

        item1 = 0
        for cation in cations:
            m_a = molalities[cation]
            beta_ca = 0
            for key in betas.keys():
                if {target_anion, cation} == set(key):
                    beta_ca = betas[key]
            c_ca = 0
            for key in cs.keys():
                if {target_anion, cation} == set(key):
                    c_ca = cs[key]
            item1 += m_a * (2 * beta_ca + z * c_ca)

        item2 = 0
        for anion in anions:
            if anion != target_anion:
                m_a = molalities[anion]
                phi_xa = 0
                for key in aa_phis.keys():
                    if set(key) == {anion, target_anion}:
                        phi_xa = aa_phis[key]['phi']

                item2_subitem1 = 0
                for cation in cations:
                    m_c = molalities[cation]
                    for tkey in aac_psis.keys():
                        if {target_anion, cation, anion} == set(tkey):
                            item2_subitem1 += m_c * aac_psis[tkey]
                item2 += m_a * (2 * phi_xa + item2_subitem1)

        item3 = 0
        for cp in cation_pairs:
            m_c1 = molalities[cp[0]]
            m_c2 = molalities[cp[1]]
            psi_ccx = 0

            # find match for psi
            for key in cca_psis.keys():
                if {cp[0], cp[1], target_anion} == set(key):
                    psi_ccx = cca_psis[key]
            item3 += m_c1 * m_c2 * psi_ccx

        item4 = 0
        for cap in cation_anion_pairs:
            ion1 = cap[0]
            ion2 = cap[1]
            m1 = molalities[ion1]
            m2 = molalities[ion2]

            c_ca = 0
            for key in cs.keys():
                if set(key) == {ion1, ion2}:
                    c_ca = cs[key]

            item4 += m1 * m2 * c_ca

        item5 = 0
        for neutral in neutrals:
            m_n = molalities[neutral]
            lambda_nx = 0

            for key in lambdas.keys():
                if {neutral, target_anion} == set(key):
                    lambda_nx = lambdas[key]

            item5 += m_n * lambda_nx

        item6 = 0
        for neutral in neutrals:
            m_n = molalities[neutral]
            for cation in cations:
                m_c = molalities[cation]

                zeta_nam = 0

                for key in zetas.keys():
                    if {target_anion, cation, neutral} == set(key):
                        zeta_nam = zetas[key]
                item6 += m_n * m_c * zeta_nam

        ln_coefficient = item0 + item1 + item2 + item3 + abs(charge_number) * item4 + 2 * item5 + item6

        return ln_coefficient

    def get_neutral_activity_coefficients(self, target_neutral, x):
        groups = self.get_component_groups(x)
        cations = groups['cations']
        anions = groups['anions']
        cation_anion_pairs = groups['cation_anion_pairs']

        molalities = self.get_molalities(x)

        lambdas = self.get_lambdas(x)
        zetas = self.get_zetas(x)

        item0 = 0
        for cation in cations:
            m_c = molalities[cation]
            lambda_nc = 0
            for key in lambdas.keys():
                if {cation, target_neutral} == set(key):
                    lambda_nc = lambdas[key]
            item0 += m_c * lambda_nc

        item1 = 0
        for anion in anions:
            m_a = molalities[anion]
            lambda_na = 0
            for key in lambdas:
                if {anion, target_neutral} == set(key):
                    lambda_na = lambdas[key]
            item1 += m_a * lambda_na

        item2 = 0
        for pair in cation_anion_pairs:
            m1 = molalities[pair[0]]
            m2 = molalities[pair[1]]

            zeta_nca = 0
            for key in zetas.keys():
                if {target_neutral, pair[0], pair[1]} == set(key):
                    zeta_nca = zetas[key]

            item2 += m1 * m2 * zeta_nca

        ln_coefficient = 2 * item0 + 2 * item1 + item2

        return ln_coefficient

    def total_gibbs_energy(self, x):
        r = 8.314
        molalities = self.get_molalities(x)
        total_g = 0
        for species in molalities.keys():
            species_type = ll.type_of_species(species)
            m_i = molalities[species]
            ln_gamma = 0
            if species_type == 0:
                ln_gamma = self.get_neutral_activity_coefficients(species, x)
            elif species_type == 1:
                ln_gamma = self.get_cation_activity_coefficients(species, x)
            elif species_type == -1:
                ln_gamma = self.get_anion_activity_coefficients(species, x)
            total_g += m_i * (0 + r * self.t * (np.log(m_i) + ln_gamma))

        # gibbs energy of water
        ln_a_w = self.get_water_activity(x)
        std_cp_water = pm.get_chemical_potential(species='H2O(l)', t=self.t)

        cp_water = (1000 / 18.015) * (std_cp_water + r * self.t * ln_a_w)

        total_g = total_g + cp_water
        return total_g

    def solubility_equilibrium(self, x):
        print(x)
        target_species = self.solids[0]
        lna_pitzer = self.get_water_activity(x)
        if target_species == 'H2O(S)':
            # lnk_ice = clegg_and_brimblecombe(self.t)
            # lnk_ice = monnin(self.t)
            lnk_ice = spencer(self.t)
            f = lnk_ice - lna_pitzer
        else:
            molalities = self.get_molalities(x)

            lnk_potential = pm.get_chemical_potential(species=target_species, t=self.t)

            solid_data = solids[target_species]
            lnk_activity = 0
            for species in solid_data.keys():
                # get the stochiometric number of this species first
                sto = solid_data[species]['value']

                if solid_data[species]['type'] == 'cation':
                    m_c = molalities[species]
                    ln_gamma_c = self.get_cation_activity_coefficients(species, x)
                    lnk_activity += sto * (np.log(m_c) + ln_gamma_c)
                elif solid_data[species]['type'] == 'anion':
                    m_a = molalities[species]
                    ln_gamma_a = self.get_anion_activity_coefficients(species, x)
                    lnk_activity += sto * (np.log(m_a) + ln_gamma_a)
                else:
                    lnk_activity += sto * lna_pitzer

            # if a neutral species should be considered.
            if self.neutral:
                ln_gamma_n = self.get_neutral_activity_coefficients(target_species, x)

                lnk_activity = (np.log(molalities[target_species]) + ln_gamma_n) - lnk_activity
            f = lnk_potential - lnk_activity
        return f

    def optimize(self):
        # Start the timer
        start_time = time.time()

        bounds = ((0, None), (0, None))
        # bounds = ((0, None))
        cons1 = {'type': 'eq', 'fun': self.charge_balance}
        cons2 = {'type': 'eq', 'fun': self.solubility_equilibrium}
        res = minimize(
            fun=self.total_gibbs_energy,
            x0=self.x0,
            method='SLSQP',
            bounds=bounds,
            constraints=(cons1, cons2)
            # constraints=(cons1)
        )

        # end of timer
        elapsed_time = time.time() - start_time
        print('times used:', elapsed_time)

        return res

    def find_x(self):
        func = lambda x: self.solubility_equilibrium(x)
        res = root(func, x0=self.x0)
        return res.x[0]
