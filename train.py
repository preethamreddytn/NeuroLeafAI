"""
Production-Ready Training Script for Plant Disease Classification

This script trains a CNN model with:
- Transfer learning (EfficientNetB0)
- Advanced data augmentation
- Learning rate scheduling
- Early stopping
- Model checkpointing
- Training visualization

Author: BioAgriCure Team
Date: 2025-11-01
"""

import os
import sys
import tensorflow as tf
from app.models.cnn_model import (
    create_cnn_model, 
    compile_model, 
    create_data_generators,
    get_callbacks,
    plot_training_history
)
from config import MODEL_PATH

# Suppress TensorFlow warnings for cleaner output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def train_model(data_dir, epochs=30, batch_size=32, learning_rate=0.001):
    """
    Train the CNN model for plant disease classification.
    
    This function implements a complete training pipeline:
    1. Load and augment data
    2. Create optimized CNN model
    3. Train with callbacks (early stopping, checkpointing, LR scheduling)
    4. Generate training plots
    5. Save best model
    
    Args:
        data_dir (str): Root directory containing train/ and validation/ folders
        epochs (int): Maximum training epochs (early stopping may end sooner)
        batch_size (int): Images per batch (32 is optimal for most GPUs)
        learning_rate (float): Initial learning rate for Adam optimizer
    
    Returns:
        tuple: (trained_model, training_history)
    """
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + "  BioAgriCure - Plant Disease Detection Training  ".center(58) + "#")
    print("#" + " "*58 + "#")
    print("#"*60 + "\n")
    
    # Step 1: Verify dataset structure
    train_dir = os.path.join(data_dir, 'train')
    validation_dir = os.path.join(data_dir, 'validation')
    
    if not os.path.exists(train_dir) or not os.path.exists(validation_dir):
        print("✗ ERROR: Dataset directories not found!")
        print("\nExpected structure:")
        print(f"{data_dir}/")
        print("├── train/")
        print("│   ├── disease_class_1/")
        print("│   ├── disease_class_2/")
        print("│   └── ...")
        print("└── validation/")
        print("    ├── disease_class_1/")
        print("    ├── disease_class_2/")
        print("    └── ...")
        print("\nPlease organize your dataset and try again.")
        return None, None
    
    print(f"✓ Dataset found: {data_dir}")
    print(f"  - Training: {train_dir}")
    print(f"  - Validation: {validation_dir}")
    
    # Step 2: Create data generators with augmentation
    train_generator, validation_generator = create_data_generators(
        train_dir, 
        validation_dir, 
        batch_size=batch_size
    )
    
    num_classes = train_generator.num_classes
    
    # Step 3: Build and compile model
    model = create_cnn_model(num_classes=num_classes)
    model = compile_model(model, learning_rate=learning_rate)
    
    # Display model architecture
    print("\n" + "="*60)
    print("MODEL ARCHITECTURE SUMMARY")
    print("="*60)
    model.summary()
    print("="*60 + "\n")
    
    # Calculate training parameters
    total_params = model.count_params()
    trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    non_trainable_params = total_params - trainable_params
    
    print("Model Parameters:")
    print(f"  • Total: {total_params:,}")
    print(f"  • Trainable: {trainable_params:,}")
    print(f"  • Non-trainable: {non_trainable_params:,}")
    print(f"  • Trainable ratio: {trainable_params/total_params*100:.1f}%")
    
    # Step 4: Setup training callbacks
    callbacks = get_callbacks(model_path=MODEL_PATH)
    
    # Step 5: Train the model
    print("\n" + "="*60)
    print("STARTING TRAINING")
    print("="*60)
    print(f"Epochs: {epochs} (may stop early if no improvement)")
    print(f"Batch size: {batch_size}")
    print(f"Initial learning rate: {learning_rate}")
    print(f"Steps per epoch: {len(train_generator)}")
    print(f"Validation steps: {len(validation_generator)}")
    print("="*60 + "\n")
    
    try:
        history = model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=callbacks,
            verbose=1  # Show progress bar
        )
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user!")
        print("Saving current model state...")
        model.save(MODEL_PATH)
        return model, None
    
    # Step 6: Generate training visualization
    if history:
        plot_training_history(history, save_path='models/training_history.png')
    
    return model, history


if __name__ == "__main__":
    # Configuration
    DATA_DIRECTORY = "data/crop_disease_dataset"
    EPOCHS = 50              # Increased - simple model needs more epochs
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001    # Standard learning rate
    
    # Welcome message
    print("\n" + "*"*60)
    print("*" + " "*58 + "*")
    print("*" + "  PRODUCTION-READY CNN TRAINING SYSTEM  ".center(58) + "*")
    print("*" + "  Plant Disease Classification Model  ".center(58) + "*")
    print("*" + " "*58 + "*")
    print("*"*60)
    
    print("\nFeatures:")
    print("  ✔ Transfer Learning (EfficientNetB0)")
    print("  ✔ Advanced Data Augmentation")
    print("  ✔ Smart Fine-Tuning (30% of base model)")
    print("  ✔ L2 Regularization")
    print("  ✔ Batch Normalization")
    print("  ✔ Dropout Layers")
    print("  ✔ Early Stopping")
    print("  ✔ Learning Rate Scheduling")
    print("  ✔ Model Checkpointing")
    print("  ✔ Training Visualization")
    print("  ✔ GPU Acceleration")
    
    print("\nDataset:")
    print(f"  • Path: {DATA_DIRECTORY}")
    print("  • Source: Kaggle (jawadali1045)")
    print("  • Size: 20,000+ images")
    print("  • Classes: 42 plant diseases")
    
    print("\nTraining Configuration:")
    print(f"  • Max Epochs: {EPOCHS}")
    print(f"  • Batch Size: {BATCH_SIZE}")
    print(f"  • Initial LR: {LEARNING_RATE}")
    print(f"  • Target: 95%+ accuracy")
    
    # Check dataset exists
    if not os.path.exists(DATA_DIRECTORY):
        print("\n" + "!"*60)
        print("✗ ERROR: Dataset directory not found!")
        print(f"  Expected: {DATA_DIRECTORY}")
        print("\nPlease:")
        print("  1. Download dataset from Kaggle:")
        print("     https://www.kaggle.com/datasets/jawadali1045/20k-multi-class-crop-disease-images")
        print(f"  2. Extract to: {DATA_DIRECTORY}")
        print("  3. Run this script again")
        print("!"*60)
        sys.exit(1)
    
    # Start training
    print("\n" + "="*60)
    print("Press Ctrl+C at any time to stop training early")
    print("="*60)
    input("\nPress ENTER to start training...")
    
    model, history = train_model(
        data_dir=DATA_DIRECTORY,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE
    )
    
    # Training complete
    if model is not None and history is not None:
        print("\n" + "#"*60)
        print("#" + " "*58 + "#")
        print("#" + "  TRAINING COMPLETED SUCCESSFULLY!  ".center(58) + "#")
        print("#" + " "*58 + "#")
        print("#"*60)
        
        print(f"\n✓ Model saved to: {MODEL_PATH}")
        print("✓ Training plots saved to: models/training_history.png")
        
        # Final summary
        final_train_acc = history.history['accuracy'][-1]
        final_val_acc = history.history['val_accuracy'][-1]
        final_train_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]
        
        print("\nFinal Metrics:")
        print(f"  • Training Accuracy: {final_train_acc*100:.2f}%")
        print(f"  • Validation Accuracy: {final_val_acc*100:.2f}%")
        print(f"  • Training Loss: {final_train_loss:.4f}")
        print(f"  • Validation Loss: {final_val_loss:.4f}")
        
        # Performance evaluation
        if final_val_acc >= 0.95:
            print("\n⭐ EXCELLENT: Target 95%+ validation accuracy achieved!")
        elif final_val_acc >= 0.90:
            print("\n✓ GREAT: Strong 90%+ validation accuracy!")
        elif final_val_acc >= 0.85:
            print("\n✓ GOOD: Solid 85%+ validation accuracy")
        else:
            print("\n⚠ Consider longer training or different hyperparameters")
        
        print("\nNext Steps:")
        print("  1. Review training plots: models/training_history.png")
        print("  2. Test model: python run.py")
        print("  3. Deploy to production")
        
    else:
        print("\n" + "!"*60)
        print("✗ Training failed or was interrupted")
        print("!"*60)
    
    print("\n" + "="*60)
    print("Thank you for using BioAgriCure!")
    print("="*60 + "\n")