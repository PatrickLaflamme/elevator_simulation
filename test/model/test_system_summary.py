from elevator_controller.model.system_summary import SystemSummary


def test_summary_stats():
    # given
    summary = SystemSummary()

    # when
    for i in range(10):
        summary.add(i)
    results = summary.__dict__()

    # then
    assert(results.get('max') == 9)
    assert(results.get('min') == 0)
    assert(results.get('mean') == 4.5)
