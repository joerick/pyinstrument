from pyinstrument import Profiler

def save_profile_to_db(profile):
    # This is where we would save the profile data to the database
    pass

def run_and_save_profile():
    profiler = Profiler()
    profiler.start()
    total = sum(range(1000))
    profiler.stop()
    save_profile_to_db(profiler.output_text())


def run_heavy_task():
    total = 0
    for i in range(10_000):
        total += i ** 2
    return total

def run_profiler_and_report():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, color=False)
    print(report)
    return report