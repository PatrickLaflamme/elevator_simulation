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
  
    
def test_summary_addition():
    summary1 = SystemSummary()
    summary1.min_value = 1
    summary1.max_value = 12
    summary1.sum = 120
    summary1.n = 15

    summary2 = SystemSummary()
    summary2.min_value = 4
    summary2.max_value = 14
    summary2.sum = 130
    summary2.n = 20

    sum_summary = summary2 + summary1

    assert sum_summary.min_value == 1
    assert sum_summary.max_value == 14
    assert sum_summary.sum == 250
    assert sum_summary.n == 35
