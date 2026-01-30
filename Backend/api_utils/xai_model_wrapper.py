import tensorflow as tf
from tensorflow.keras.models import Model

def get_differentiable_model(original_model):
    """
    Reconstructs the model graph starting AFTER the embedding lookup.
    Input: [Emb_Country, Emb_Sector, Emb_Sub, Emb_Gas, Numerical]
    Output: Prediction
    """
    # 1. Define New Inputs
    # Shapes must match the output of your Embedding layers: (Sequence_Length, Embedding_Dim)
    # Based on your summary: Seq=12, EmbDim=8
    seq_len = 12
    emb_dim = 8
    num_dim = 6 
    
    # We use 'None' for batch size to allow flexibility
    in_emb_country = tf.keras.Input(shape=(seq_len, emb_dim), name="xai_country")
    in_emb_sector = tf.keras.Input(shape=(seq_len, emb_dim), name="xai_sector")
    in_emb_subsector = tf.keras.Input(shape=(seq_len, emb_dim), name="xai_subsector")
    in_emb_gas = tf.keras.Input(shape=(seq_len, emb_dim), name="xai_gas")
    in_numerical = tf.keras.Input(shape=(seq_len, num_dim), name="xai_numerical")
    
    # 2. Re-connect the Graph
    # We fetch layers by name from the trained model to reuse their weights
    
    # Step A: Concatenate Embeddings
    concat_layer_1 = original_model.get_layer("concatenate") 
    # Note: Ensure the order matches your original creation order!
    x_cat = concat_layer_1([in_emb_country, in_emb_sector, in_emb_subsector, in_emb_gas])
    
    # Step B: Concatenate with Numerical
    concat_layer_2 = original_model.get_layer("concatenate_1")
    x = concat_layer_2([x_cat, in_numerical])
    
    # Step C: Projection & Positional Encoding
    x = original_model.get_layer("dense")(x) # Projection
    x = original_model.get_layer("positional_embedding")(x)
    
    # Step D: Transformer Blocks
    # Dynamically find encoder layers to be robust
    for layer in original_model.layers:
        if "transformer_encoder" in layer.name:
            x = layer(x)
            
    # Step E: Output Head
    x = original_model.get_layer("dense_5")(x) # Output dense
    output = original_model.get_layer("lambda")(x) # Squeeze
    
    # 3. Create the Wrapper Model
    new_model = Model(
        inputs=[in_emb_country, in_emb_sector, in_emb_subsector, in_emb_gas, in_numerical],
        outputs=output,
        name="Differentiable_GHG_Model"
    )
    
    return new_model