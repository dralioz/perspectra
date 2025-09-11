# Fine-Tuning U^2-Net for Your Use Case

## 🎯 **Objective**
Fine-tune U^2-Net specifically for document/perspective correction to achieve:
- **10-50x faster inference** (from 1s to 20-100ms)
- **Smaller model size** (from 168MB to 10-50MB)
- **Better accuracy** for your specific use case

## 📋 **Prerequisites**

```bash
# Install training dependencies
pip install torch torchvision 
pip install albumentations
pip install segmentation-models-pytorch
pip install wandb  # for experiment tracking
```

## 📂 **Data Preparation**

### 1. **Dataset Structure**
```
dataset/
├── images/          # Original images
│   ├── img_001.jpg
│   ├── img_002.jpg
│   └── ...
├── masks/           # Ground truth masks  
│   ├── img_001.png  # Binary masks (0=background, 255=object)
│   ├── img_002.png
│   └── ...
└── splits/
    ├── train.txt    # Training image names
    ├── val.txt      # Validation image names
    └── test.txt     # Test image names
```

### 2. **Data Collection Strategy**
- **Documents:** Collect 500-2000 document images
- **Angles:** Various perspectives (top-down, angled, skewed)
- **Backgrounds:** Different surfaces, lighting conditions  
- **Quality:** Mix of phone photos, scanned docs, etc.

## 🔧 **Fine-Tuning Script**

### Create training script:

```python
# fine_tune_u2net.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import segmentation_models_pytorch as smp
from pathlib import Path
import albumentations as A
from albumentations.pytorch import ToTensorV2

class DocumentDataset:
    def __init__(self, image_dir, mask_dir, image_list, transform=None):
        self.image_dir = Path(image_dir)
        self.mask_dir = Path(mask_dir)
        self.image_list = image_list
        self.transform = transform
    
    def __len__(self):
        return len(self.image_list)
    
    def __getitem__(self, idx):
        # Load image and mask
        img_name = self.image_list[idx]
        image = cv2.imread(str(self.image_dir / img_name))
        mask = cv2.imread(str(self.mask_dir / img_name.replace('.jpg', '.png')), 0)
        
        if self.transform:
            transformed = self.transform(image=image, mask=mask)
            image = transformed['image']
            mask = transformed['mask']
        
        return image.float() / 255.0, mask.float() / 255.0

# Training configuration
def get_training_config():
    return {
        'model_name': 'U2NET_lite',  # Lighter version
        'input_size': (224, 224),    # Smaller input for speed
        'batch_size': 16,
        'learning_rate': 1e-4,
        'epochs': 100,
        'early_stopping': 15,
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    }

def create_transforms(input_size):
    train_transform = A.Compose([
        A.Resize(*input_size),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.3),
        A.Rotate(limit=15, p=0.3),
        A.Normalize(),
        ToTensorV2()
    ])
    
    val_transform = A.Compose([
        A.Resize(*input_size),
        A.Normalize(),
        ToTensorV2()
    ])
    
    return train_transform, val_transform

def train_model():
    config = get_training_config()
    
    # Create model (lightweight U-Net)
    model = smp.Unet(
        encoder_name="mobilenet_v2",        # Lightweight encoder
        encoder_weights="imagenet",
        in_channels=3,
        classes=1,
    )
    
    # Training loop
    # ... (implement training logic)
    
    # Export to ONNX for inference
    torch.onnx.export(
        model,
        torch.randn(1, 3, *config['input_size']),
        "custom_document_segmentation.onnx",
        export_params=True,
        opset_version=11,
        input_names=['input'],
        output_names=['output']
    )

if __name__ == "__main__":
    train_model()
```

## ⚡ **Quick Performance Gains**

### 1. **Use Lite Models Immediately**
```python
# Instead of u2net (168MB), use:
config = PerspectraConfig(
    model_type="u2net_lite",  # ~4MB, 10x faster
    image_size=(224, 224),    # Smaller input = faster
    ort_intra_op_num_threads=2
)
```

### 2. **Model Quantization**
```python
# Quantize existing model for 2-4x speedup
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

# Quantize model
quantize_dynamic(
    "u2net_lite.onnx",
    "u2net_lite_quantized.onnx", 
    weight_type=QuantType.QUInt8
)
```

### 3. **Input Size Optimization**
```python
# Test different input sizes for speed/accuracy tradeoff
sizes_to_test = [
    (160, 160),  # Very fast, lower quality
    (224, 224),  # Good balance  
    (320, 320),  # Better quality, slower
]
```

## 📊 **Expected Performance Improvements**

| Optimization | Speed Gain | Size Reduction | Accuracy Impact |
|-------------|------------|----------------|----------------|
| U2Net Lite | 10-15x | 168MB → 4MB | -5% |
| Custom Fine-tune | 20-50x | 168MB → 10-30MB | +10-20% |
| Quantization | 2-4x | 50% smaller | -1-3% |
| Smaller Input | 2-5x | Same | -5-10% |

## 🚀 **Production Deployment**

### Custom Model Integration
```python
# Use your fine-tuned model
config = PerspectraConfig(
    model_type="custom",
    model_filename="your_finetuned_model.onnx",
    image_size=(224, 224),
    use_quantized=True
)

processor = PerspectraProcessor(config)
```

## 🎯 **Recommended Approach**

1. **Immediate (Today):** Switch to `u2net_lite` → 10x speedup
2. **Short-term (1-2 weeks):** Collect domain-specific data
3. **Medium-term (1 month):** Fine-tune lightweight model
4. **Long-term (2-3 months):** Custom architecture + quantization

Would you like me to help you implement any of these optimizations?
