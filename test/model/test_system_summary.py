from elevator_controller.model.system_summary import SystemSummary


def test_summary_stats():
    # given
    summary = SystemSummary()

    # when
    for i in range(10):
        summary.include(i)
    results = summary.__dict__()

    # then
    assert(results.get('max') == 9)
    assert(results.get('min') == 0)
    assert(results.get('mean') == 4.5)


def test_empty_summary_stats():
    # given
    summary = SystemSummary()

    # when
    results = summary.__dict__()

    # then
    assert(results.get('max') == None)
    assert(results.get('min') == None)
    assert(results.get('mean') == 0.0)
