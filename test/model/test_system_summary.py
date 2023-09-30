from elevator_controller.model.system_summary import SystemSummary


def test_summary_stats():
    summary = SystemSummary()
    for i in range(10):
        summary.add(i)
    assert(summary.max_value == 9)
    assert(summary.min_value == 0)
    assert(summary.mean() == 4.5)
    results = summary.__dict__()
    assert(results.get('max') == 9)
    assert(results.get('min') == 0)
    assert(results.get('mean') == 4.5)
