config = {
    "getaway": "https://api.wakatime.com/api/v1",
    "all_time_since_today": {
        "method": "get",
        "uri": "/users/{}/all_time_since_today" # user
    },
    "commit": {
        "method": "get",
        "uri": "/users/{}/projects/{}/commits/{}" # user, project, hash
    },
    "commits": {
        "method": "get",
        "uri": "/users/{}/projects/{}/commits" # user, project
    },
    "custom_rules": {
        "method": "get",
        "uri": "/users/{}/custom_rules" # user
    },
    "custom_rules_progress": {
        "method": "get",
        "uri": "/users/{}/custom_rules_progress" # user
    },
    "data_dumps": {
        "method": "get",
        "uri": "/users/{}/data_dumps" # user
    },
    "durations": {
        "method": "get",
        "uri": "/users/{}/durations" # user
    },
    "external_durations": {
        "method": "get",
        "uri": "/users/{}/external_durations" # user
    },
    "editors": {
        "method": "get",
        "uri": "/editors"
    },
    "goal": {
        "method": "get",
        "uri": "/users/{}/goals/{}" # user, goal
    },
    "goals": {
        "method": "get",
        "uri": "/users/{}/goals" # user
    },
    "heartbeats": {
        "method": "get",
        "uri": "/users/{}/heartbeats" # user
    },
    "insights": {
        "method": "get",
        "uri": "/users/{}/insights/{}/{}" # user, insight_type, range
    },
    "leaders": {
        "method": "get",
        "uri": "/leaders"
    },
    "machine_names": {
        "method": "get",
        "uri": "/users/{}/machine_names" # user
    },
    "meta": {
        "method": "get",
        "uri": "/meta"
    },
    "org_custom_rules": {
        "method": "get",
        "uri": "/users/{}/orgs/{}/custom_rules" # user, org
    },
    "org_dashboard_durations": {
        "method": "get",
        "uri": "users/{}/orgs/{}/dashboards/{}/durations" # user, org, dashboard
    },
    "org_dashboard_member_durations": {
        "method": "get",
        "uri": "/users/{}/orgs/{}/dashboards/{}/members/{}/durations" # user, org, dashboard, member
    },
    "org_dashboard_member_summaries": {
        "method": "get",
        "uri": "/users/{}/orgs/{}/dashboards/{}/members/{}/summaries" # user, org, dashboard, member
    },
    "org_dashboard_members": {
        "method": "get",
        "uri": "/users/{}/orgs/{}/dashboards/{}/members" # user, org, dashboard
    },
    "org_dashboard_summaries": {
        "method": "get",
        "uri": "/users/{}/orgs/{}/dashboards/{}/summaries" # user, org, dashboard
    },
    "org_dashboards": {
        "method": "get",
        "uri": "/users/{}/orgs/{}/dashboards" # user, org
    },
    "orgs": {
        "method": "get",
        "uri": "/users/{}/orgs" # user
    },
    "private_leaderboards": {
        "method": "get",
        "uri": "/users/{}/leaderboards" # user
    },
    "private_leaderboard_leaders": {
        "method": "get",
        "uri": "/users/{}/leaderboards/{}" # user, board
    },
    "program_languages": {
        "method": "get",
        "uri": "/program_languages"
    },
    "projects": {
        "method": "get",
        "uri": "/users/{}/projects" # user
    },
    "stats": {
        "method": "get",
        "uri": "/users/{}/stats" # user, '/range/{}' <- range
    },
    "stats_aggregated": {
        "method": "get",
        "uri": "/stats/{}" # range
    },
    "status_bar": {
        "method": "get",
        "uri": "/users/{}/status_bar/{}" # user, range
    },
    "summaries": {
        "method": "get",
        "uri": "/users/{}/summaries" # user
    },
    "user_agents": {
        "method": "get",
        "uri": "/users/{}/user_agents" # user
    },
    "users": {
        "method": "get",
        "uri": "/users/{}" # user
    }
}