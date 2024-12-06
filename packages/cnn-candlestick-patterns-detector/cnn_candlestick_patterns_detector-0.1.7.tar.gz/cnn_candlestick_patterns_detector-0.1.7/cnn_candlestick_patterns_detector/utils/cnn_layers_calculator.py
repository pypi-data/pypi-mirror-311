import torch.nn as nn


def calculate_output_shape(input_shape, conv_layers):
    c, h, w = input_shape
    for layer in conv_layers:
        if isinstance(layer, nn.Conv2d):
            padding = layer.padding if isinstance(layer.padding, tuple) else (layer.padding, layer.padding)
            kernel_size = layer.kernel_size if isinstance(layer.kernel_size, tuple) else (
                layer.kernel_size, layer.kernel_size)
            stride = layer.stride if isinstance(layer.stride, tuple) else (layer.stride, layer.stride)

            h = (h + 2 * padding[0] - kernel_size[0]) // stride[0] + 1
            w = (w + 2 * padding[1] - kernel_size[1]) // stride[1] + 1
            c = layer.out_channels
            print(f"After Conv2d: c={c}, h={h}, w={w}")
        elif isinstance(layer, nn.ConvTranspose2d):
            padding = layer.padding if isinstance(layer.padding, tuple) else (layer.padding, layer.padding)
            kernel_size = layer.kernel_size if isinstance(layer.kernel_size, tuple) else (
                layer.kernel_size, layer.kernel_size)
            stride = layer.stride if isinstance(layer.stride, tuple) else (layer.stride, layer.stride)
            output_padding = layer.output_padding if isinstance(layer.output_padding, tuple) else (
                layer.output_padding, layer.output_padding)

            h = (h - 1) * stride[0] - 2 * padding[0] + kernel_size[0] + output_padding[0]
            w = (w - 1) * stride[1] - 2 * padding[1] + kernel_size[1] + output_padding[1]
            c = layer.out_channels
            print(f"After ConvTranspose2d: c={c}, h={h}, w={w}")
        elif isinstance(layer, nn.MaxPool2d):
            padding = layer.padding if isinstance(layer.padding, tuple) else (layer.padding, layer.padding)
            kernel_size = layer.kernel_size if isinstance(layer.kernel_size, tuple) else (
                layer.kernel_size, layer.kernel_size)
            stride = layer.stride if isinstance(layer.stride, tuple) else (layer.stride, layer.stride)

            h = (h + 2 * padding[0] - kernel_size[0]) // stride[0] + 1
            w = (w + 2 * padding[1] - kernel_size[1]) // stride[1] + 1
            print(f"After MaxPool2d: c={c}, h={h}, w={w}")
    return c, h, w


input_shape = (4, 3, 4)
conv_layers = [
    nn.ConvTranspose2d(4, 8, kernel_size=3, stride=1, padding=1),
    nn.ConvTranspose2d(8, 16, kernel_size=3, stride=2, padding=1, output_padding=1),
    nn.ConvTranspose2d(16, 8, kernel_size=3, stride=1, padding=1),
    nn.ConvTranspose2d(8, 1, kernel_size=(2, 3), stride=1, padding=1),
]

output_shape = calculate_output_shape(input_shape, conv_layers)
print(f"Output shape after Conv2d and layers: {output_shape}")
