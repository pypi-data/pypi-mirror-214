import unittest
from copy import deepcopy
from unittest.mock import MagicMock, call

from netboxkea.kea.app import DHCP4App
from netboxkea.kea.exceptions import KeaClientError, SubnetNotFound


class TestKea(unittest.TestCase):

    def _set_std_subnet(self):
        self.kea.set_subnet(100, {'subnet': '192.168.0.0/24'})

    def _set_std_resa(self):
        self.kea.set_reservation(100, 200, {
            'ip-address': '192.168.0.1', 'hw-address': '11:22:33:44:55:66',
            'hostname': 'pc.lan'})

    def _set_std_pool(self):
        self.kea.set_pool(100, 250, {'pool': '192.168.0.100-192.168.0.199'})

    def setUp(self):
        self.kea = DHCP4App('http://keasrv/api')
        self.req = MagicMock()
        self.kea.api._request_kea = self.req
        self.srv_conf = {'Dhcp4': {}}
        self.srv_check_res = True

        def req_result(cmd, params=None):
            match cmd:
                case 'config-get':
                    return deepcopy(self.srv_conf)
                case 'config-set':
                    self.srv_conf = deepcopy(params)
                case 'config-test':
                    return self.srv_check_res
                case 'config-write':
                    pass
                case _:
                    raise ValueError(cmd)

        self.req.side_effect = req_result
        self.kea.pull()
        self.req.reset_mock()

    def test_01_pull(self):
        self.assertEqual(self.kea.conf, {'subnet4': []})
        self.assertEqual(self.kea.commit_conf, self.kea.conf)

    def test_02_commit(self):
        newconf = {'subnet4': [{'garbage': True}]}
        self.kea.conf = deepcopy(newconf)
        self.kea.commit()
        self.req.assert_called_once_with('config-test', {'Dhcp4': newconf})
        self.assertEqual(self.kea.conf, self.kea.commit_conf)

    def test_03_push_wo_commit(self):
        self.kea.push()
        self.req.assert_not_called()

    def test_04_push_w_commit(self):
        newconf = {'subnet4': [{'garbage': True}]}
        self.kea.conf = deepcopy(newconf)
        self.kea.commit()
        self.kea.push()
        calls = [call('config-test', {'Dhcp4': newconf}),
                 call('config-set', {'Dhcp4': newconf}),
                 call('config-write', {'Dhcp4': newconf})]
        self.req.has_calls(calls)
        self.assertEqual(self.srv_conf['Dhcp4'], newconf)
        self.assertEqual(self.kea.conf, self.kea.commit_conf)

    def test_10_set_subnet(self):
        expected = {'subnet4': [
            {'id': 100, 'subnet': '192.168.0.0/24', 'pools': [],
             'reservations': []}]}
        self._set_std_subnet()
        self.kea.push()
        self.assertEqual(self.srv_conf['Dhcp4'], expected)

    def test_11_set_subnet_replace(self):
        self.kea.set_subnet(100, {'subnet': '10.0.0.0/8'})
        self._set_std_subnet()
        self.kea.push()
        self.assertEqual(
            self.srv_conf['Dhcp4']['subnet4'][0]['subnet'], '192.168.0.0/24')
        self.assertEqual(len(self.srv_conf['Dhcp4']['subnet4']), 1)

    def test_12_set_subnet_conflict(self):
        self._set_std_subnet()
        with self.assertRaises(KeaClientError):
            self.kea.set_subnet(101, {'subnet': '192.168.0.0/24'})

    def test_13_update_subnet_notfound(self):
        with self.assertRaises(SubnetNotFound):
            self.kea.update_subnet(100, {'subnet': '10.0.0.0/8', 'opt': 1})

    def test_14_update_subnet_ok(self):
        self._set_std_subnet()
        self.kea.update_subnet(100, {'subnet': '192.168.0.0/24', 'opt': 1})
        self.kea.push()
        self.assertEqual(self.srv_conf['Dhcp4']['subnet4'][0]['opt'], 1)

    def test_15_del_subnet(self):
        self._set_std_subnet()
        self.kea.del_subnet(100)
        self.kea.push()
        self.assertEqual(len(self.srv_conf['Dhcp4']['subnet4']), 0)

    def test_16_del_all_subnets(self):
        self._set_std_subnet()
        self.kea.del_all_subnets()
        self.kea.push()
        self.assertEqual(len(self.srv_conf['Dhcp4']['subnet4']), 0)

    def test_20_set_reservation(self):
        expected = {'subnet4': [
            {'id': 100, 'subnet': '192.168.0.0/24', 'pools': [],
             'reservations': [{
                'ip-address': '192.168.0.1', 'hw-address': '11:22:33:44:55:66',
                'hostname': 'pc.lan', 'user-context': {
                    'netbox_ip_address_id': 200}}]
             }]}
        self._set_std_subnet()
        self._set_std_resa()
        self.kea.push()
        self.assertEqual(self.srv_conf['Dhcp4'], expected)

    def test_21_set_reservation_replace(self):
        self._set_std_subnet()
        self._set_std_resa()
        self.kea.set_reservation(100, 200, {
            'ip-address': '192.168.0.9', 'hw-address': '11:22:33:44:55:66',
            'hostname': 'pc.lan'})
        self.kea.push()
        self.assertEqual(
            self.srv_conf['Dhcp4']['subnet4'][0]['reservations'][0]
            ['ip-address'], '192.168.0.9')
        self.assertEqual(len(
            self.srv_conf['Dhcp4']['subnet4'][0]['reservations']), 1)

    def test_22_set_reservation_subnet_not_found(self):
        with self.assertRaises(SubnetNotFound):
            self._set_std_resa()

    def test_23_set_reservation_conflict_hw(self):
        self._set_std_subnet()
        self._set_std_resa()
        with self.assertRaises(KeaClientError):
            self.kea.set_reservation(100, 201, {
                'ip-address': '192.168.0.2', 'hw-address': '11:22:33:44:55:66',
                'hostname': 'pc2.lan'})

    def test_24_set_reservation_conflict_ip(self):
        self._set_std_subnet()
        self._set_std_resa()
        with self.assertRaises(KeaClientError):
            self.kea.set_reservation(100, 201, {
                'ip-address': '192.168.0.1', 'hw-address': '11:22:33:33:22:11',
                'hostname': 'pc2.lan'})

    def test_25_set_reservation_no_conflict_ip(self):
        self.srv_conf['Dhcp4']['ip-reservations-unique'] = False
        self.kea.pull()
        self._set_std_subnet()
        self._set_std_resa()
        self.kea.set_reservation(100, 201, {
            'ip-address': '192.168.0.1', 'hw-address': '11:22:33:33:22:11',
            'hostname': 'pc2.lan'})
        self.assertEqual(len(self.kea.conf['subnet4'][0]['reservations']), 2)

    def test_26_del_reservation(self):
        self._set_std_subnet()
        self._set_std_resa()
        self.kea.del_resa(200)
        self.assertEqual(len(self.kea.conf['subnet4'][0]['reservations']), 0)

    def test_30_set_pool(self):
        expected = {'subnet4': [
            {'id': 100, 'subnet': '192.168.0.0/24', 'pools': [{
                'pool': '192.168.0.100-192.168.0.199',
                'user-context': {'netbox_ip_range_id': 250}
                }], 'reservations': []}]}
        self._set_std_subnet()
        self._set_std_pool()
        self.kea.push()
        self.assertEqual(self.srv_conf['Dhcp4'], expected)

    def test_33_set_pool_conflict_overlap(self):
        self._set_std_subnet()
        self._set_std_pool()
        with self.assertRaises(KeaClientError):
            self.kea.set_pool(100, 251, {'pool': '192.168.0.50-192.168.0.100'})
        with self.assertRaises(KeaClientError):
            self.kea.set_pool(100, 251, {
                'pool': '192.168.0.199-192.168.0.250'})

    def test_35_del_pool(self):
        self._set_std_subnet()
        self._set_std_pool()
        self.kea.del_pool(250)
        self.assertEqual(len(self.kea.conf['subnet4'][0]['pools']), 0)
