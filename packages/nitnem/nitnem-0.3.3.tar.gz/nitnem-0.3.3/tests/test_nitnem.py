from nitnem import cli


def test_create_parser():
    parser = cli.create_parser()
    result = parser.parse_args([])
    assert result.audio_choice == "auto"
    assert result.audio_file is None
    assert result.delay_duration == 3


def test_create_parser_with_ac():
    parser = cli.create_parser()
    result = parser.parse_args(["-ac", "sukhmani"])
    assert result.audio_choice == "sukhmani"
    assert result.audio_file is None
