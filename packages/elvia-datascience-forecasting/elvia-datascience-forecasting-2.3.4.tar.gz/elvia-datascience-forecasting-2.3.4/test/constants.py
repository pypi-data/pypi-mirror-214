import random


model_ids = ['0028', '9999', 'TextBasedæøå789']
model_target_ids = {
    '0028': ['0028-TR1', '0028-TR2'],
    '9999': ['ENS10191T1', 'ENS10261T2', 'ENS10133T1', 'ENS10461T1'],
    'TextBasedæøå789': [random.randint(707057500014300000, 707057500087400700) for _ in range(0,20)]
}
