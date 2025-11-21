((*- extends 'article.tplx' -*))

((* block docclass *))\documentclass[11pt]{article}((* endblock docclass *))

((* block title *)){{ resources.metadata.get('title', 'ru-it-audit-report') }}((* endblock title *))

((* block author *)){{ resources.metadata.get('author', 'run-as-daemon.ru') }}((* endblock author *))

((* block packages *))
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}
\usepackage{longtable}
((* endblock packages *))
