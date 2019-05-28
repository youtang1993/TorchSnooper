import io
import torch
import torchsnooper
from .utils import assert_output, VariableEntry, CallEntry, LineEntry, ReturnEntry, OpcodeEntry, ReturnValueEntry, ExceptionEntry


def test_default_tensor():
    string_io = io.StringIO()

    @torchsnooper.snoop(string_io)
    def my_function():
        x = torch.randn((5, 8), requires_grad=True)
        return x

    my_function()

    output = string_io.getvalue()
    print(output)
    assert_output(
        output,
        (
            CallEntry(),
            LineEntry(),
            VariableEntry('x', 'tensor<(5, 8), float32, cpu, grad>'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('tensor<(5, 8), float32, cpu, grad>'),
        )
    )


def test_tensor_property_selector():
    string_io = io.StringIO()
    fmt = torchsnooper.TensorFormat(properties=('shape', 'device', 'requires_grad'))

    @torchsnooper.snoop(string_io, tensor_format=fmt)
    def my_function():
        x = torch.randn((5, 8))
        return x

    my_function()

    output = string_io.getvalue()
    print(output)
    assert_output(
        output,
        (
            CallEntry(),
            LineEntry(),
            VariableEntry('x', 'tensor<(5, 8), cpu>'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('tensor<(5, 8), cpu>'),
        )
    )


def test_tensor_property_name():
    string_io = io.StringIO()
    fmt = torchsnooper.TensorFormat(property_name=True)

    @torchsnooper.snoop(string_io, tensor_format=fmt)
    def my_function():
        x = torch.randn((5, 8))
        return x

    my_function()

    output = string_io.getvalue()
    print(output)
    assert_output(
        output,
        (
            CallEntry(),
            LineEntry(),
            VariableEntry('x', 'tensor<shape=(5, 8), dtype=float32, device=cpu, requires_grad=False>'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('tensor<shape=(5, 8), dtype=float32, device=cpu, requires_grad=False>'),
        )
    )