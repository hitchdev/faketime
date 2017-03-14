Python:
  preconditions:
    files:
      fake.py: |
        from commandlib import Command
        import faketime
        import datetime

        faketime.change_time("newtime.txt", datetime.datetime(2050, 6, 7, 10, 9, 22, 123456))

        python = Command("python")
        print_date = python("-c", "import datetime ; print datetime.datetime.now()")
        print_date_in_future = print_date.with_env(**faketime.get_environment_vars("newtime.txt"))
        print_date_in_future.run()
  scenario:
    - Run:
        cmd: python /faketime/example/fake.py
        expect: 2050
