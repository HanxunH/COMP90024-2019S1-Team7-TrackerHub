import torch

file_path = 'checkpoints/food179_resnet101_sgd_v3.pth_best.pth'
checkpoint = torch.load(file_path, map_location=lambda storage, loc: storage)
model_class_to_idx = checkpoint['class_to_idx']
print(model_class_to_idx)
for item in model_class_to_idx:
    if model_class_to_idx[item] == 83:
        model_class_to_idx['gyudon'] = model_class_to_idx.pop(item)

print(len(model_class_to_idx), model_class_to_idx['gyudon'])
print(model_class_to_idx)
model_idx_to_class = {v: k for k, v in model_class_to_idx.items()}
print(len(model_idx_to_class))


# checkpoint['class_to_idx'] = model_class_to_idx
# torch.save(checkpoint, file_path)
