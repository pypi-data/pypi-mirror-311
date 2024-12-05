def add_gradient_weighted(grad1, grad2, w2):
    return [
        g1 + g2 * w2 for g1, g2 in zip(grad1, grad2)
    ]

def divide_gradients(gradients, divider):
    return [
        g / divider for g in gradients
    ]

def multiply_gradients(gradients, factor):
    return [
        g * factor for g in gradients
    ]
