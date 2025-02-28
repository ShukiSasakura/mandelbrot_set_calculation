#!/usr/bin/bash

# make logfile
dateandtime=$(date '+%Y%m%d-%H%M%S')
touch ./log/native/$dateandtime.log
touch ./log/wasmtime/$dateandtime.log
touch ./log/wasmer/$dateandtime.log

# execute native implement
for i in `seq 40`
do
    command='./target/release/mandelblot_set -w 20000 -h 15000 -t $i >> ./log/native/$dateandtime.log'
    echo 'execute native implement'
    echo $command
    $command
done

sleep 2

# execute wasmtime implement
for i in `seq 40`
do
    command='wasmtime -S threads ./target/wasm32-wasip1-threads/release/mandelblot_set.wasm -w 20000 -h 15000 -t $i >> ./log/wasmtime/$dateandtime.log'
    echo 'execute wasmtime implement'
    echo $command
    $command
done

sleep 2

# execute wasmer implement
for i in `seq 40`
do
    command='wasmer ./target/wasm32-wasmer-wasi/release/mandelblot_set.wasm -- -w 20000 -h 15000 -t $i >> ./log/wasmer/$dateandtime.log'
    echo 'execute wasmer implement'
    echo $command
    $command
done

