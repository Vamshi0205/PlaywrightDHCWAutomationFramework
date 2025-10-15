def register_cli(parser):
    grp = parser.getgroup("fwk")
    grp.addoption("--env", action="store", default="qa", help="Environment: dev/qa/prod")
    grp.addoption("--headed", action="store_true", help="Run headed browser")