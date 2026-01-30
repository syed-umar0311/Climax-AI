import tensorflow as tf
import numpy as np

def get_gradients(model, inputs_list):
    """
    Computes gradients of the model's output prediction with respect to the input features.
    """
    # Convert inputs to tensors if they aren't already
    inputs_tensors = [tf.convert_to_tensor(x, dtype=tf.float32) for x in inputs_list]
    
    with tf.GradientTape() as tape:
        tape.watch(inputs_tensors)
        # Forward pass
        predictions = model(inputs_tensors)
        
    # Calculate gradients of the prediction w.r.t inputs
    grads = tape.gradient(predictions, inputs_tensors)
    return grads

def compute_integrated_gradients(model, baseline_inputs, target_inputs, steps=50):
    """
    Approximates the integral of gradients (Integrated Gradients).
    """
    alphas = np.linspace(0, 1, steps + 1)
    
    # 1. Generate interpolated inputs along the path
    interpolated_path = []
    
    # We loop over each input feature type (Country, Sector, ..., Numerical)
    for i in range(len(baseline_inputs)):
        start = baseline_inputs[i] # Shape: (1, 12, 8)
        end = target_inputs[i]     # Shape: (1, 12, 8)
        delta = end - start
        
        # --- CRITICAL FIX: BROADCASTING DIMENSIONS ---
        # We need alpha to look like (Steps, 1, 1, 1) to broadcast correctly 
        # against (1, 12, 8) -> Resulting in (Steps, 1, 12, 8)
        
        # Add a '1' for every dimension in the input
        alpha_shape = [steps + 1] + [1] * len(start.shape)
        alphas_reshaped = alphas.reshape(alpha_shape)
        
        # Linear interpolation
        path_inputs = start + alphas_reshaped * delta
        interpolated_path.append(path_inputs)

    # 2. Compute Gradients for every step along the path
    grads_sum = [np.zeros_like(inp[0]) for inp in baseline_inputs]
    
    # Process step-by-step
    for step in range(steps + 1):
        # Extract the inputs for this step
        # path[step] will now correctly be (1, 12, 8) because of the fix above
        current_inputs = [path[step] for path in interpolated_path]
        
        step_grads = get_gradients(model, current_inputs)
        
        for i, g in enumerate(step_grads):
            if g is not None:
                # Accumulate
                grads_sum[i] += g.numpy()[0] # [0] to remove batch dim for summation

    # 3. Average Gradients and Multiply by Delta
    attributions = []
    for i in range(len(baseline_inputs)):
        avg_grads = grads_sum[i] / (steps + 1)
        
        # delta is (1, 12, 8), avg_grads is (12, 8)
        # We remove batch dim from delta for the math
        delta_squeezed = (target_inputs[i] - baseline_inputs[i])[0]
        
        # IG = (Input - Baseline) * AverageGradient
        attr = delta_squeezed * avg_grads
        attributions.append(attr.numpy())
        
    return attributions