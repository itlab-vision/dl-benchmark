# Оптимизация модели средствами Apache TVM

## Описание скрипта

### Основная информация

Директория содержит набор скриптов для запуска трех моделей оптимизации сетей из Apache TVM: autotvm, auto-scheduler, meta-schedule.

## Использование скрипта

Пример запуска tvm_autotvm.py: 

```bash
python tvm_autotvm.py -m mod.json -p param.params -t "llvm" -l autotvm.log
```

Пример запуска tvm_auto_scheduler.py: 

```bash
python tvm_auto_scheduler.py -m mod.json -p param.params \ 
       -t "llvm -mcpu=core-avx2" -l auto-scheduler.log -n 64
```

Пример запуска tvm_meta_schedule.py: 

```bash
python tvm_meta_schedule.py -m mod.json -p param.params \ 
       -t "llvm  -mcpu=core-avx2 --num-cores=6" -w metasc -n 64 \
       --max_trials_per_task 128
```

Для получения более подробной информации:

```bash
python <script.py> -h
```