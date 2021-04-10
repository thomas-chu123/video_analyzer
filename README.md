# video_analyzer

##### **Purpose:**
The tool is used on Windows platform to monitor the IPTV stream quality (packet loss, jitter, delay, etc) 
by using Tshark (Wireshark command line interface) to capture 60 second RTP data and analysing them.
The tool will also send IGMPv3 join the join the multicast channel before capture the IPTV data.
The GUI interface (tinker module) will help you to configure the required setting.
After the analysing, the analyzed result will be exported to excel file to monitor the long term quality on IPTV channel.

##### **Requirement:**
1. Python3
2. Tshark (make sure /tshark is included in the subdirectory)
3. xlsxwriter (python module running with source code)
4. netifaces (python module running with source code)

###### **Execution:**
1. Use video_check.exe to execute the tool

