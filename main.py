import scripts.requirements as requirements, scripts.portScan as portScan, scripts.vulnerabilities as vulnerabilities, scripts.installer as installer

def main():
	requirements.install()
	portScan.perform()
	installer.start()
	vulnerabilities.start()
	return 0

if __name__ == "__main__":
	main()
