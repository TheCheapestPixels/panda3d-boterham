from direct.showbase.ShowBase import ShowBase
from .property_logic import evaluate_property_logic


base = ShowBase(windowType='none')

def postprocess(filename):
    print('post-processing', filename)
    root = loader.load_model(filename)
    evaluate_property_logic(root)
    root.write_bam_file(filename)
