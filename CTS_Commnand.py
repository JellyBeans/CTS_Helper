#result = os.system('xterm -e "echo exit -c | /home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed run cts -c android.bluetooth.cts.BluetoothLeScanTest -m testBatchScan --skip-preconditions | /home/ray/test1.log"')

#os.system("/home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed run cts -c android.bluetooth.cts.BluetoothLeScanTest -m testBatchScan --skip-preconditions | tee /home/ray/test.log")
import subprocess

#method 3
#ild = subprocess.Popen(["/home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed","run", "cts", "-c", "android.bluetooth.cts.BluetoothLeScanTest", "-m", "testBatchScan", "--skip-preconditions"],stdout=subprocess.PIPE,start_new_session=True)
#out = child.communicate()


child = subprocess.Popen(["xterm","-e","/home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed run cts -c android.bluetooth.cts.BluetoothLeScanTest -m testBatchScan --skip-preconditions" ],stdout=subprocess.PIPE,start_new_session=True)
out = child.communicate()
print("---->",out)