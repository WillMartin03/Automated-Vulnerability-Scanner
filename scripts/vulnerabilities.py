import os, platform, subprocess

output = []

def createList():
	portlist = []
	try:
		with open("./ports.txt", "r") as f:
			for line in f:
				line = line.strip()
				if line == "\x90":
					break
				portlist.append(line)
		return portlist
	except Exception as e:
		print(e)
		print("Error detected, exiting...")
		exit()

def start():
	print("Start Vulnerability Scan...")
	portlist = createList()
	for i in range(1, len(portlist)):
		scan(portlist[0], portlist[i])
	print("Vulnerability Scan Complete! Please check the output below:")
	if (len(output) == 0):
		print("No vulnerabilities found.")
	else:
		for line in output:
			print(line)

	# Remove 'ports.txt' so next time the program is run the user can enter new information
	os.remove("./ports.txt")

def scanModule(module, ip, port):
	print(f"Scanning {ip}:{port} with {module.split('/')[-1]}...")
	if platform.system() == "Windows":
		pre = "C:\\Tools\\metasploit-framework\\bin\\"
		ext = ".bat"
	else:
		pre = ""
		ext = ""

	result = subprocess.run(
		f"{pre}msfconsole{ext} -q -x \"use {module}; set RHOSTS {ip}; set RPORT {port}; run; exit\"",
		shell=True,
		capture_output=True,
		text=True,
	)

	for line in result.stdout.splitlines():
		if "[+]" in line:
			line = line.replace("[+]", "").strip()
			line = f"[VULNERABLE]: {module.split('/')[-1]} - {line}"
			output.append(line)

	with open("./output.txt", "a") as f:
		f.write(f"Scanning {ip}:{port} with {module.split('/')[-1]}...\n")
		for line in result.stdout.splitlines():
			f.write(line + "\n")
		f.write("\n")

	return result

def scan(ip, port):
	modules = [
		"auxiliary/scanner/http/http_version", # CVE-2014-7230, HTTP Version Detection
		"auxiliary/scanner/http/dir_scanner", # CVE-2014-8877, Directory Scanner
		"auxiliary/scanner/http/files_dir", # CVE-2014-8877, Files Directory Scanner
		"auxiliary/scanner/http/verb_auth_bypass", # CVE-2014-8877, Verb Auth Bypass
		"auxiliary/scanner/http/robots_txt", # CVE-2014-2563, Robots.txt Scanner
		"auxiliary/scanner/http/options", # CVE-2014-5256, HTTP Options Method Detection
		"auxiliary/scanner/http/http_put", # CVE-2014-0050, HTTP PUT Method Detection
		"auxiliary/scanner/http/webdav_scanner", # CVE-2017-7269, WebDAV Scanner
		"auxiliary/scanner/http/wordpress_scanner", # CVE-2015-1579, WordPress Scanner
		"auxiliary/scanner/http/wordpress_content_injection", # CVE-2015-1579, WordPress Content Injection
		"auxiliary/scanner/ssl/openssl_heartbleed", # CVE-2014-0160, Heartbleed Vulnerability
	]

	for module in modules:
		result = scanModule(module, ip, port)
		if result.returncode == 0:
			print(result.stdout)
		else:
			print(result.stderr)

	return

if __name__ == "__main__":
	print(f"Starting from {os.path.basename(__file__)}. This is usually for developer purposes, please make sure this is intentional.\nIf you want to run the full program, please execute the 'main.py' file instead.")
	start()