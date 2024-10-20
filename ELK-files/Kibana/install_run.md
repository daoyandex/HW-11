Start Kibana
Run bin/kibana (or bin\kibana.bat on Windows)

Open Kibana
Click on the link provided in the terminal, or point your browser at 
http://localhost:5601 
and follow enrollment instructions to connect to Elasticsearch



n:~/kibana-8.15.2/bin$ ./kibana
Kibana is currently running with legacy OpenSSL providers enabled! For details and instructions on how to disable see https://www.elastic.co/guide/en/kibana/8.15/production.html#openssl-legacy-provider
{"log.level":"info","@timestamp":"2024-10-14T23:36:28.401Z","log.logger":"elastic-apm-node","ecs.version":"8.10.0","agentVersion":"4.7.0","env":{"pid":105015,"proctitle":"./../node/glibc-217/bin/node","os":"linux 6.1.0-26-amd64","arch":"x64","host":"debian","timezone":"UTC+0300","runtime":"Node.js v20.15.1"},"config":{"active":{"source":"start","value":true},"breakdownMetrics":{"source":"start","value":false},"captureBody":{"source":"start","value":"off","commonName":"capture_body"},"captureHeaders":{"source":"start","value":false},"centralConfig":{"source":"start","value":false},"contextPropagationOnly":{"source":"start","value":true},"environment":{"source":"start","value":"production"},"globalLabels":{"source":"start","value":[["git_rev","5a522bfe14bc6d06c20bc337477fd53f7c538973"]],"sourceValue":{"git_rev":"5a522bfe14bc6d06c20bc337477fd53f7c538973"}},"logLevel":{"source":"default","value":"info","commonName":"log_level"},"metricsInterval":{"source":"start","value":120,"sourceValue":"120s"},"serverUrl":{"source":"start","value":"https://kibana-cloud-apm.apm.us-east-1.aws.found.io/","commonName":"server_url"},"transactionSampleRate":{"source":"start","value":0.1,"commonName":"transaction_sample_rate"},"captureSpanStackTraces":{"source":"start","sourceValue":false},"secretToken":{"source":"start","value":"[REDACTED]","commonName":"secret_token"},"serviceName":{"source":"start","value":"kibana","commonName":"service_name"},"serviceVersion":{"source":"start","value":"8.15.2","commonName":"service_version"}},"activationMethod":"require","message":"Elastic APM Node.js Agent v4.7.0"}
Native global console methods have been overridden in production environment.
[2024-10-15T02:36:29.142+03:00][INFO ][root] Kibana is starting
[2024-10-15T02:36:29.161+03:00][INFO ][node] Kibana process configured with roles: [background_tasks, ui]
[2024-10-15T02:36:32.876+03:00][INFO ][plugins-service] The following plugins are disabled: "cloudChat,cloudExperiments,cloudFullStory,profilingDataAccess,profiling,securitySolutionServerless,serverless,serverlessObservability,serverlessSearch".
[2024-10-15T02:36:32.912+03:00][INFO ][http.server.Preboot] http server running at http://localhost:5601
[2024-10-15T02:36:32.981+03:00][INFO ][plugins-system.preboot] Setting up [1] plugins: [interactiveSetup]
[2024-10-15T02:36:32.988+03:00][INFO ][preboot] "interactiveSetup" plugin is holding setup: Validating Elasticsearch connection configuration…
[2024-10-15T02:36:33.005+03:00][INFO ][root] Holding setup until preboot stage is completed.


i Kibana has not been configured.

Go to http://localhost:5601/?code=314881 to get started.





user@debian:~$ sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token --scope kibana

eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTcyLjE3LjAuMTo5MjAwIl0sImZnciI6ImMwZWEzMjllMmY0NmQwZTI2ZWQxOGM4YWM4ZjFkN2VhNTg4MjAyM2Q3NDZlY2MxMzM1MDU0NjJlYjA2OWUyMzIiLCJrZXkiOiJqcTlwalpJQlNUd2JMWmZGN1ZKQzpiQ2xRamxsQlNHYUZkaDZpU3l4UTRRIn0=


Connect to
https://localhost:9200
Username: kibana_system