import os
import json
import shutil
import tempfile

from blend2bam import blenderutils
from blend2bam.common import ConverterBase


# NOTE: all of this is only here as monkeypatch to add the --python-use-system-env arg

def run_blender_script(script, args, blenderdir='', blenderbin='blender'):
    blenderutils.run_blender(
        [
            '--python-use-system-env',
            '-P', script,
            '--',
        ] + args,
        blenderdir=blenderdir,
        blenderbin=blenderbin
    )


class ConverterBlend2Gltf28(ConverterBase):
    script_file = os.path.join(os.path.dirname(__file__), 'blender28_script.py')

    def convert_single(self, src, dst):
        srcroot = os.path.dirname(src)
        dstdir = os.path.dirname(dst)
        files = [
            src
        ]
        self.convert_batch(srcroot, dstdir, files)

        dstout = os.path.join(dstdir, os.path.basename(src).replace('.blend', '.gltf'))
        shutil.move(dstout, dst)

    def convert_batch(self, srcroot, dstdir, files):
        blenderdir = self.settings.blender_dir
        settings_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump(self.settings._asdict(), settings_file)
        settings_file.close() # Close so the tempfile can be re-opened in Blender on Windows
        args = [
            settings_file.name,
            srcroot,
            dstdir,
        ] + files
        run_blender_script(self.script_file, args, blenderdir=blenderdir)
        os.remove(settings_file.name)
