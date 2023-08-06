import unittest
from pathlib import Path

from gcscore import CommandRenderer, ScriptTemplatesExtension
from gcscore.mod import Visitor

from gcsaws import NodeRunInOrder, flatten, NodeRunInParallel
from gcsaws.visitor_overview import VisitorStateOverview, setup_visitor_overview


class TestProcedureFlattening(unittest.TestCase):
    def test_run_in_order_tree(self):
        parent = NodeRunInOrder(name='a')
        aa = parent.run_in_order('aa')
        aaa = aa.pause('aaa')
        aab = aa.pause('aaa')
        ab = parent.run_in_order('ab')
        aba = ab.pause('aba')

        flatten(parent)
        self.assertEqual(3, len(parent.gcscore_children))
        self.assertEqual(aaa, parent.gcscore_children[0])
        self.assertEqual(aab, parent.gcscore_children[1])
        self.assertEqual(aba, parent.gcscore_children[2])

    def test_run_in_order_depth(self):
        parent = NodeRunInOrder(name='a')
        aa = parent.run_in_order('aa')
        aaa = aa.pause('aaa')
        aab = aa.run_in_order('aab')
        aaba = aab.pause('aaba')
        aabb = aab.pause('aabb')
        aabc = aab.pause('aabc')
        aabd = aab.run_in_order('aabd')
        aabda = aabd.pause('aabda')
        ab = parent.pause('ab')
        ac = parent.pause('ac')
        ad = parent.run_in_order('ad')
        ada = ad.pause('ada')

        flatten(parent)
        self.assertEqual(8, len(parent.gcscore_children))
        self.assertEqual(aaa, parent.gcscore_children[0])
        self.assertEqual(aaba, parent.gcscore_children[1])
        self.assertEqual(aabb, parent.gcscore_children[2])
        self.assertEqual(aabc, parent.gcscore_children[3])
        self.assertEqual(aabda, parent.gcscore_children[4])
        self.assertEqual(ab, parent.gcscore_children[5])
        self.assertEqual(ac, parent.gcscore_children[6])
        self.assertEqual(ada, parent.gcscore_children[7])

    def test_run_in_order_mono_child_async(self):
        parent = NodeRunInOrder(name='a')
        aa = parent.pause('aa')
        ab = parent.run_in_parallel('ab')
        aba = ab.pause('aba')

        flatten(parent)
        self.assertEqual(2, len(parent.gcscore_children))
        self.assertEqual(aa, parent.gcscore_children[0])
        self.assertEqual(aba, parent.gcscore_children[1])

    def test_run_in_order_async_with_run_in_order_child(self):
        parent = NodeRunInOrder(name='a')
        aa = parent.pause('aa')
        ab = parent.run_in_parallel('ab')
        aba = ab.run_in_order('aba')
        abaa = aba.pause('abaa')

        flatten(parent)
        self.assertEqual(2, len(parent.gcscore_children))
        self.assertEqual(aa, parent.gcscore_children[0])
        self.assertEqual(abaa, parent.gcscore_children[1])

    def test_run_in_parallel_tree(self):
        parent = NodeRunInParallel(name='a')
        aa = parent.pause('aa')
        ab = parent.run_in_parallel('ab')
        aba = ab.pause('aba')
        abb = ab.pause('abb')
        ac = parent.run_in_parallel('ac')
        aca = ac.pause('aca')

        flatten(parent)
        self.assertEqual(4, len(parent.gcscore_children))
        self.assertEqual(aa, parent.gcscore_children[0])
        self.assertEqual(aba, parent.gcscore_children[1])
        self.assertEqual(abb, parent.gcscore_children[2])
        self.assertEqual(aca, parent.gcscore_children[3])

    def test_run_in_order_with_one_async_child_with_multiple_children(self):
        parent = NodeRunInOrder(name='a')
        aa = parent.run_in_parallel('aa')
        aaa = aa.pause('aaa')
        aab = aa.pause('aab')

        flatten(parent)
        self.assertEqual(1, len(parent.gcscore_children))
        self.assertEqual(aa, parent.gcscore_children[0])
        self.assertEqual(2, len(parent.gcscore_children[0].gcscore_children))
        self.assertEqual(aaa, parent.gcscore_children[0].gcscore_children[0])
        self.assertEqual(aab, parent.gcscore_children[0].gcscore_children[1])

    def test_complexity_1(self):
        patching_qas = NodeRunInOrder(name='patching_qas')
        pause_start = patching_qas.pause('pause_start')
        send_start_message = patching_qas.pause('send_start_message')
        patch_os_in_parallel = patching_qas.run_in_parallel('patch_os_in_parallel')

        patch_linux = patch_os_in_parallel.run_in_order('patch_linux')
        stop_qas_linux_1 = patch_linux.run_in_order('stop_qas_linux_1')
        stop_os_separately_linux = stop_qas_linux_1.run_in_parallel('stop_os_separately_linux')
        stop_qas_linux = stop_os_separately_linux.run_in_order('stop_qas_linux')
        stop_vtom_backup = stop_qas_linux.pause('stop_vtom_backup')
        stop_qas_servers_linux = stop_qas_linux.run_in_parallel('stop_qas_servers_linux')
        stop_desvaws1911 = stop_qas_servers_linux.pause('stop_desvaws1911')
        stop_desvaws1913 = stop_qas_servers_linux.pause('stop_desvaws1913')
        stop_desvaws1916 = stop_qas_servers_linux.pause('stop_desvaws1916')
        stop_desvawssap19050 = stop_qas_servers_linux.pause('stop_desvawssap19050')
        stop_qas_web_dispatchers = stop_qas_linux.run_in_parallel('stop_qas_web_dispatchers')
        stop_desvaws1710 = stop_qas_web_dispatchers.pause('stop_desvaws1710')
        verify_cloud_registration = patch_linux.pause('verify_cloud_registration')
        disable_swap = patch_linux.pause('disable_swap')
        take_snapshots_linux = patch_linux.pause('take_snapshots_linux')
        apply_patches_linux = patch_linux.pause('apply_patches_linux')
        enable_swap = patch_linux.pause('enable_swap')
        start_qas_linux_1 = patch_linux.run_in_order('start_qas_linux_1')
        start_os_separately_linux = start_qas_linux_1.run_in_parallel('start_os_separately_linux')
        start_qas_linux = start_os_separately_linux.run_in_order('start_qas_linux')
        start_qas_web_dispatchers = start_qas_linux.run_in_parallel('start_qas_web_dispatchers')
        start_desvaws1710 = start_qas_web_dispatchers.pause('start_desvaws1710')
        start_qas_servers_linux = start_qas_linux.run_in_parallel('start_qas_servers_linux')
        start_desvaws1911 = start_qas_servers_linux.pause('start_desvaws1911')
        start_desvaws1913 = start_qas_servers_linux.pause('start_desvaws1913')
        start_desvaws1916 = start_qas_servers_linux.pause('start_desvaws1916')
        start_desvawssap19050 = start_qas_servers_linux.pause('start_desvawssap19050')
        start_vtom = start_qas_linux.pause('start_vtom')

        patch_windows = patch_os_in_parallel.run_in_order('patch_windows')
        stop_qas_windows = patch_windows.run_in_order('stop_qas_windows')
        stop_os_separately_windows = stop_qas_windows.run_in_parallel('stop_os_separately_windows')
        stop_qas_servers_windows = stop_os_separately_windows.run_in_parallel('stop_qas_servers_windows')
        stop_desvawssap19071 = stop_qas_servers_windows.pause('stop_desvawssap19071')
        stop_bods = stop_qas_servers_windows.run_in_order('stop_bods')
        stop_desvaws1919 = stop_bods.pause('stop_desvaws1919')
        stop_desvaws1918 = stop_bods.pause('stop_desvaws1918')
        take_snapshots_windows = patch_windows.pause('take_snapshots_windows')
        apply_patches_windows = patch_windows.pause('apply_patches_windows')
        start_qas_windows = patch_windows.run_in_order('start_qas_windows')
        start_os_separately_windows = start_qas_windows.run_in_parallel('start_os_separately_windows')
        start_qas_servers_windows = start_os_separately_windows.run_in_parallel('start_qas_servers_windows')
        start_desvawssap19071 = start_qas_servers_windows.pause('start_desvawssap19071')
        start_bods = start_qas_servers_windows.run_in_order('start_bods')
        start_desvaws1919 = start_bods.pause('start_desvaws1919')
        start_desvaws1918 = start_bods.pause('start_desvaws1918')

        send_end_message = patching_qas.pause('send_end_message')

        cmd_renderer = CommandRenderer()
        ScriptTemplatesExtension.configure(cmd_renderer)

        visitor_state = VisitorStateOverview(100)
        visitor = Visitor()
        setup_visitor_overview(visitor)
        visitor.visit(patching_qas, visitor_state)
        result_before_flatten = visitor_state.export_html()
        Path('data/patching_qas.plain.overview.html').write_text(result_before_flatten, encoding='utf-8')

        flatten(patching_qas)

        visitor_state = VisitorStateOverview(100)
        visitor = Visitor()
        setup_visitor_overview(visitor)
        visitor.visit(patching_qas, visitor_state)
        result_after_flatten = visitor_state.export_html()
        Path('data/patching_qas.flat.overview.html').write_text(result_after_flatten, encoding='utf-8')


        self.assertEqual(
            [
                pause_start,
                send_start_message,
                patch_os_in_parallel,
                send_end_message
            ],
            patching_qas.gcscore_children
        )

        final_patch_os_in_parallel = patching_qas.gcscore_children[2]
        self.assertEqual(
            [
                patch_linux,
                patch_windows
            ],
            final_patch_os_in_parallel.gcscore_children
        )

        final_patch_linux = final_patch_os_in_parallel.gcscore_children[0]
        self.assertEqual(
            [
                stop_vtom_backup,
                stop_qas_servers_linux,
                stop_desvaws1710,
                verify_cloud_registration,
                disable_swap,
                take_snapshots_linux,
                apply_patches_linux,
                enable_swap,
                start_desvaws1710,
                start_qas_servers_linux,
                start_vtom
            ],
            final_patch_linux.gcscore_children
        )

        final_patch_windows = final_patch_os_in_parallel.gcscore_children[1]
        self.assertEqual(
            [
                stop_os_separately_windows,
                take_snapshots_windows,
                apply_patches_windows,
                start_os_separately_windows
            ],
            final_patch_windows.gcscore_children
        )
