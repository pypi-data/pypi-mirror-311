import pytest
from pysongtool import PySongTool
from pysongtool.exceptions.UnknownChord import UnknownChord
from pysongtool.exceptions.WrongNote import WrongNote
from pysongtool.exceptions.UnknownScale import WrongScale

@pytest.fixture
def pysongtool_instance():
    return PySongTool()

def test_chord_valid(pysongtool_instance):
    result = pysongtool_instance.chord('C', 'maj')
    expected_notes = ['C', 'E', 'G']
    assert result['notes'] == expected_notes
    assert result['chord'] == 'Cmaj'

def test_chord_invalid_chord(pysongtool_instance):
    with pytest.raises(UnknownChord):
        pysongtool_instance.chord('C', 'unknown')

def test_chord_invalid_note(pysongtool_instance):
    with pytest.raises(WrongNote):
        pysongtool_instance.chord('H', 'maj')

def test_all_chords(pysongtool_instance):
    result = pysongtool_instance.all_chords('C')
    assert len(result) > 0
    assert 'maj' in result[0]

def test_scale_valid(pysongtool_instance):
    result = pysongtool_instance.scale('C', 'major')
    expected_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert result['notes'] == expected_notes

def test_scale_invalid_scale(pysongtool_instance):
    with pytest.raises(WrongScale):
        pysongtool_instance.scale('C', 'unknown')

def test_scale_invalid_note(pysongtool_instance):
    with pytest.raises(WrongNote):
        pysongtool_instance.scale('H', 'major')

def test_intervals(pysongtool_instance):
    result = pysongtool_instance.intervals('C')
    assert result[0]['note'] == 'C'
    assert result[0]['semitones'] == 0

def test_intervals_invalid_note(pysongtool_instance):
    with pytest.raises(WrongNote):
        pysongtool_instance.intervals('H')

def test_get_interval(pysongtool_instance):
    result = pysongtool_instance.get_intervals('C', 'E', 'G')
    assert result[0]['note'] == 'E'
    assert result[0]['interval']['semitones'] == 4

def test_get_interval_invalid_note(pysongtool_instance):
    with pytest.raises(WrongNote):
        pysongtool_instance.get_intervals('C', 'H')
