import onnx
import torch

from onnx_pytorch.op_code_generators import OpCodeGenerator


class SigmoidOpCodeGenerator(OpCodeGenerator):

  def __init__(self,
               onnx_ver=onnx.defs.onnx_opset_version(),
               torch_ver=torch.__version__):
    super(SigmoidOpCodeGenerator, self).__init__(onnx_ver, torch_ver)

  def gen(self, node, value_infos, initializers, rename_helper, tensor_inplace):
    inputs_str, outputs_str = self.gen_input_output_string(
        node, initializers, rename_helper, tensor_inplace)
    init_str, forward_str = [], []
    node_name = rename_helper.get_node_name(node.name, node.op_type)
    init_str.append(f"self.{node_name} = nn.{self.onnx_op}()")
    forward_str.append(f"{outputs_str[0]} = self.{node_name}({inputs_str[0]})")
    return {"init": init_str, "forward": forward_str}
