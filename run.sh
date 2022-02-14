#!/usr/bin/env bash

# TODO: Add more projects
for PROJECT in camel  # kafka spark thrift arrow geode hbase beam
do
    pushd study && \
    python -m collect_jira_issues $PROJECT && \
    python -m collect_vcs_history $PROJECT && \
    python -m compute_stats $PROJECT
done

popd;

montage -density 300 -tile 3x0 -geometry +5+50 data/output/*.png data/output/all_stats.png
