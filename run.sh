dateandtime=$(date '+%Y%m%d-%H%M%S')
# native
touch ./log/native/$dateandtime.log
touch ./log/wasm/$dateandtime.log
for i in `seq 40`
do
./target/release/mandelblot_set -w 20000 -h 15000 -t $i >> ./log/native/$dateandtime.log
done

# wasm
for i in `seq 40`
do
wasmer ./target/wasm32-wasmer-wasi/release/mandelblot_set.wasm -- -w 20000 -h 15000 -t $i >> ./log/wasm/$dateandtime.log
done
