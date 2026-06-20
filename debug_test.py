import subprocess, tempfile, json, os, time

data = {
    'domain': 'machine_learning',
    'algorithm': 'vqe',
    'hpc': True,
    'num_qubits': 16,
    'problem': {
        'orbital_energies': [0.1] * 16
    }
}

f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
json.dump(data, f)
f.close()

print(f'File: {f.name}')

wsl_file = subprocess.run(['wsl', 'wslpath', '-u', f.name], capture_output=True, text=True).stdout.strip()
print(f'WSL Path: {wsl_file}')

binary = r'C:\Users\IMRAN\Downloads\nawaz1-server'
wsl_bin = subprocess.run(['wsl', 'wslpath', '-u', binary], capture_output=True, text=True).stdout.strip()
print(f'Binary: {wsl_bin}')

env = 'NAWAZ1_MODE=serverless NAWAZ1_INPUT_FILE="{}" JWT_SECRET="test-32-chars-secret-key" RUST_LOG=warn'.format(wsl_file)

print(f'\nRunning...')
t0 = time.perf_counter()
r = subprocess.run(['wsl', 'bash', '-c', '{} {}'.format(env, wsl_bin)], capture_output=True, text=True, timeout=60)
elapsed = (time.perf_counter() - t0) * 1000

print(f'Time: {elapsed:.0f}ms')
print(f'Return code: {r.returncode}')
print(f'STDOUT length: {len(r.stdout)}')
print(f'\nFirst 500 chars of STDOUT:')
print(r.stdout[:500])
print(f'\nSTDERR:')
print(r.stderr[:300])

os.unlink(f.name)
