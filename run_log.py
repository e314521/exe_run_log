import subprocess
import sys

from pathlib import Path

def execute_cmd(command):
    try:
        # 执行命令并捕获输出
        result = subprocess.run(command, shell=True, check=False, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              encoding='GBK',
                              text=True)
        
        # 获取命令的输出
        output = result.stdout
        # 如果有错误信息，也获取错误信息
        error = result.stderr
        return result.returncode, output, error
    except subprocess.CalledProcessError as e:
        return 1, None, str(e)

def safe_join(command_list):
    """
    将一个参数列表安全地连接成一个命令行字符串。
    这是对 shlex.join() 的一个简单替代，用于旧版Python。
    """
    # 如果是 Python 3.8+，优先使用内置的 shlex.join
    if sys.version_info >= (3, 8):
        import shlex
        return shlex.join(command_list)
    
    # 对于旧版本，手动实现
    # subprocess.list2cmdline 是一个很好的替代品，虽然不是完全一样，但目的相同
    # 注意：list2cmdline 是 Windows 风格的引号处理
    return subprocess.list2cmdline(command_list)


def run_and_log_fastboot(command_exe, command_args):
    """
    执行 fastboot 命令并记录其输出和错误。
    :param command_args: 一个列表，包含命令和所有参数，例如 ['flash', 'boot', 'boot.img']
    """
    
    command_path = Path(command_exe)
    command_path = command_path.with_stem(command_path.stem + "-old").with_suffix(".exe")
    command_string = subprocess.list2cmdline([str(command_path.as_posix())] + command_args)
    log_file_path = command_path.with_suffix(".log") 
    with open(log_file_path, 'a', encoding='utf-8') as f:
    # 打印要执行的命令，shlex.join 可以将列表安全地转换为命令行字符串
        f.write(f"Executing: {command_string}\r\n")
        #os.system(command_string) 
        code, output, error = execute_cmd([str(command_path.as_posix())] + command_args)
        f.write(f"Code: {code}\r\n")
        if output:
            f.write(f"Output: {output}\r\n")    
            sys.stdout.write(output)
        if error:
            f.write(f"Error: {error}\r\n")
            sys.stderr.write(error)
        return code
    return 1

if __name__ == '__main__':        
    sys.exit(run_and_log_fastboot(sys.argv[0], sys.argv[1:])) 
