def assert_lines_are_similar(s1, s2):
    # compare results
    expected_list = s1.split()
    results_list = s2.split()
    assert len(results_list) == len(expected_list)

    # assert same line number
    assert results_list[0] == expected_list[0], 'line numbers do not match'

    # timestamp almost equals
    assert abs(float(results_list[1]) - float(expected_list[1])) < 0.1

    # the rest of the list matches
    for x, y in zip(results_list[2:], expected_list[2:]):
        assert x == y
