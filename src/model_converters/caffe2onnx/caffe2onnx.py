import subprocess

def call_caffe_to_onnx_converter(caffe_proto_file, caffe_weight_file, onnx_file_name):
    script_path = 'path_to_your_script/convert_to_onnx.py'
    
    command = [
        'python', script_path, 
        caffe_proto_file, 
        caffe_weight_file, 
        onnx_file_name
    ]
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при вызове скрипта: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)


call_caffe_to_onnx_converter(
    'path/to/your/caffe_model.prototxt',
    'path/to/your/caffe_model.caffemodel',
    'path/to/save/your_model.onnx'
)
