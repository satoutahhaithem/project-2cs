import subprocess

if __name__ == '__main__':
    file1_process = subprocess.Popen(['python', 'controlRobot.py'])
    file2_process = subprocess.Popen(['python', 'liveStream.py'])

    file1_process.wait()
    file2_process.wait()
