import re
import typing

import pytest

from space_tracer import LivePng, LivePillowImage, LivePainter
from space_tracer.canvas import Canvas
from space_tracer.live_image import LiveImageDiffer
from space_tracer.mock_turtle import MockTurtle

# noinspection PyUnresolvedReferences
from test_mock_turtle import patched_turtle
from test_report_builder import trim_report

try:
    from PIL import Image
    from PIL import ImageDraw
except ImportError:
    Image = ImageDraw = None


def replace_image(report):
    report = trim_report(report)
    report = re.sub(r"image='[a-zA-Z0-9+/=]*'", "image='...'", report)
    return report


def test_display(patched_turtle):
    assert patched_turtle

    expected_report = """\
create_image
    0
    0
    image='UE5HX0lNQUdFX0RBVEE='
"""

    t = MockTurtle()
    image_data = b'PNG_IMAGE_DATA'

    LivePng(image_data).display()

    report = t.report

    assert report == expected_report.splitlines()


def test_display_position(patched_turtle):
    assert patched_turtle

    expected_report = """\
create_image
    100
    -200
    image='UE5HX0lNQUdFX0RBVEE='
"""

    t = MockTurtle()
    image_data = b'PNG_IMAGE_DATA'

    LivePng(image_data).display((100, 200))

    report = t.report

    assert report == expected_report.splitlines()


def test_display_with_size():
    expected_report = """\
create_image
    100
    200
    image='UE5HX0lNQUdFX0RBVEE='
"""

    MockTurtle.monkey_patch(Canvas(width=200, height=400))
    try:
        t = MockTurtle()
        image_data = b'PNG_IMAGE_DATA'

        LivePng(image_data).display()

        report = t.report
    finally:
        MockTurtle.remove_monkey_patch()

    assert report == expected_report.splitlines()


def test_display_image_position_with_size():
    expected_report = """\
create_image
    110
    180
    image='UE5HX0lNQUdFX0RBVEE='
"""

    MockTurtle.monkey_patch(Canvas(width=200, height=400))
    try:
        t = MockTurtle()
        image_data = b'PNG_IMAGE_DATA'

        LivePng(image_data).display((10, 20))

        report = t.report
    finally:
        MockTurtle.remove_monkey_patch()

    assert report == expected_report.splitlines()


def test_display_not_patched():
    expected_report = ""

    t = MockTurtle()
    image_data = b'PNG_IMAGE_DATA'

    LivePng(image_data).display()

    report = t.report

    assert report == expected_report.splitlines()


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_display_pillow_image(patched_turtle):
    assert patched_turtle

    image = Image.new('RGB', (2, 2))
    expected_report = """\
create_image
    0
    0
    image='...'
"""

    t = MockTurtle()

    LivePillowImage(image).display()

    report = t.report

    assert replace_image(report) == expected_report


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
@pytest.mark.parametrize('align,position',
                         [('topleft', (100, 200)),
                          ('bottomleft', (100, 220)),
                          ('topright', (110, 200)),
                          ('centerleft', (100, 210)),
                          ('topcenter', (105, 200)),
                          ('top', (105, 200)),
                          ('left', (100, 210))])
def test_display_image_bottom_left(patched_turtle,
                                   align: str,
                                   position: typing.Tuple[int, int]):
    assert patched_turtle

    image = Image.new('RGB', (10, 20))
    expected_report = """\
create_image
    100
    -200
    image='...'
"""

    t = MockTurtle()

    LivePillowImage(image).display(position, align)

    report = t.report

    assert replace_image(report) == expected_report


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_display_image_bad_align(patched_turtle):
    assert patched_turtle

    image = Image.new('RGB', (10, 20))

    with pytest.raises(ValueError, match="Invalid align: 'topfloop'."):
        LivePillowImage(image).display(align='topfloop')


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_live_pillow_pixels():
    default = (0, 0, 0, 0)
    blue = (0, 0, 255, 255)

    image = LivePillowImage(Image.new('RGBA', (10, 20)))
    image.set_pixel((5, 10), blue)
    p1 = image.get_pixel((5, 10))
    p2 = image.get_pixel((6, 10))

    assert p1 == blue
    assert p2 == default


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_live_png_as_painter(tmp_path):
    blue = (0, 0, 255, 255)
    white = (255, 255, 255, 255)

    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), blue)
    image1.set_pixel((6, 10), white)

    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image2.set_pixel((5, 10), blue)
    bytes2 = image2.convert_to_png()
    image3 = LivePng(bytes2)
    painter3 = image3.convert_to_painter()
    painter3.set_pixel((6, 10), white)

    differ = LiveImageDiffer(tmp_path)

    differ.assert_equal(image1, painter3, 'live_png_as_painter')


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare():
    dark_blue = (0, 0, 150, 255)
    medium_blue = (0, 0, 200, 255)
    bright_blue = (0, 0, 250, 255)
    expected_dark_diff = (255, 0, (150+200)//5, 255)
    expected_match = (0, 0, 200, 255//3)
    expected_bright_diff = (255, 255, (250+200)//5, 255)

    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), dark_blue)
    image1.set_pixel((6, 10), medium_blue)
    image1.set_pixel((7, 10), bright_blue)
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image2.set_pixel((5, 10), medium_blue)
    image2.set_pixel((6, 10), medium_blue)
    image2.set_pixel((7, 10), medium_blue)

    differ = LiveImageDiffer()

    diff = differ.compare(image1, image2).convert_to_painter()

    diff_pixel1 = diff.get_pixel((5, 10))
    diff_pixel2 = diff.get_pixel((6, 10))
    diff_pixel3 = diff.get_pixel((7, 10))

    assert diff_pixel1 == expected_dark_diff
    assert diff_pixel2 == expected_match
    assert diff_pixel3 == expected_bright_diff
    assert differ.diff_count == 2


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_compare_pixel_alpha_channel_missing():

    image1 = LivePillowImage(Image.new('RGB', (100, 200)))
    image2 = LivePillowImage(Image.new('RGB', (100, 200)))

    differ = LiveImageDiffer()
    differ.compare(image1, image2)


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_no_offset():
    differ = LiveImageDiffer()
    offset = 0
    differ.tolerance = 20

    image1 = LivePillowImage(Image.new('RGBA', (200, 200)))
    draw1 = ImageDraw.Draw(image1.image)
    draw1.rectangle((50, 50, 100, 100), fill='blue')
    image2 = LivePillowImage(Image.new('RGBA', (200, 200)))
    draw2 = ImageDraw.Draw(image2.image)
    draw2.rectangle((50+offset, 50, 100, 100), fill='blue')

    differ.compare(image1, image2)

    assert differ.diff_count == 0


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_offset():
    differ = LiveImageDiffer()
    offset = 1
    differ.tolerance = 20

    image1 = LivePillowImage(Image.new('RGBA', (200, 200)))
    draw1 = ImageDraw.Draw(image1.image)
    draw1.rectangle((50, 50, 100, 100), fill='blue')
    image2 = LivePillowImage(Image.new('RGBA', (200, 200)))
    draw2 = ImageDraw.Draw(image2.image)
    draw2.rectangle((50+offset, 50, 100, 100), fill='blue')

    differ.compare(image1, image2)

    assert differ.diff_count == 51


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_offset_blurred():
    differ = LiveImageDiffer()
    offset = 1
    differ.tolerance = 20
    differ.blur_radius = 5

    image1 = LivePillowImage(Image.new('RGBA', (200, 200)))
    draw1 = ImageDraw.Draw(image1.image)
    draw1.rectangle((50, 50, 100, 100), fill='blue')
    image2 = LivePillowImage(Image.new('RGBA', (200, 200)))
    draw2 = ImageDraw.Draw(image2.image)
    draw2.rectangle((50+offset, 50, 100, 100), fill='blue')

    differ.compare(image1, image2)

    assert differ.diff_count == 0


# noinspection DuplicatedCode
def test_differ_blurred_not_pillow():
    differ = LiveImageDiffer()
    differ.blur_radius = 5

    image = LivePng(b'PNG_BYTES1')

    with pytest.raises(RuntimeError,
                       match=r'LivePng cannot be blurred\. Override '
                             r'LiveImageDiffer\.blur\(\)\.'):
        # noinspection PyTypeChecker
        differ.blur(image)


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is not None, reason='Pillow not installed.')
def test_differ_blurred_pillow_not_installed():
    differ = LiveImageDiffer()
    differ.blur_radius = 5

    image = LivePillowImage(None)

    with pytest.raises(RuntimeError,
                       match=r'Pillow is not installed\. Install or override '
                             r'LiveImageDiffer\.blur\(\)\.'):
        differ.blur(image)


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_display(patched_turtle):
    assert patched_turtle

    expected_report = """\
create_text
    -1
    20
    anchor='sw'
    fill='black'
    font=('Arial', 10, 'normal')
    text='Actual'
create_image
    0
    20
    image='...'
create_text
    -1
    60
    anchor='sw'
    fill='black'
    font=('Arial', 10, 'normal')
    text='Diff (0 pixels)'
create_image
    0
    60
    image='...'
create_text
    -1
    100
    anchor='sw'
    fill='black'
    font=('Arial', 10, 'normal')
    text='Expected'
create_image
    0
    100
    image='...'
"""

    t = MockTurtle()

    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    differ = LiveImageDiffer()

    differ.compare(image1, image2)

    report = t.report

    assert replace_image(report) == expected_report


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_display_disabled(patched_turtle):
    assert patched_turtle

    expected_report = '\n'

    t = MockTurtle()

    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    differ = LiveImageDiffer(is_displayed=False)

    differ.compare(image1, image2)

    report = t.report

    assert replace_image(report) == expected_report


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_writes_file(tmp_path):
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), (0, 0, 255, 255))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    diffs_path = tmp_path / 'image_diffs'
    actual_path = diffs_path / 'test_name-actual.png'
    diff_path = diffs_path / 'test_name-diff.png'
    expected_path = diffs_path / 'test_name-expected.png'
    differ = LiveImageDiffer(diffs_path)

    differ.compare(image1, image2, 'test_name')

    assert actual_path.exists()
    assert diff_path.exists()
    assert expected_path.exists()


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_uses_test_name(tmp_path, request):
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), (0, 0, 123, 255))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    diffs_path = tmp_path / 'image_diffs'
    actual_path = (diffs_path / 'test-PySrc-tests-test_live_image-py--'
                                'test_differ_compare_uses_test_name-actual.png')
    differ = LiveImageDiffer(diffs_path, request)

    differ.compare(image1, image2)

    assert actual_path.exists()


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_test_name_without_path():
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))

    differ = LiveImageDiffer()

    with pytest.raises(ValueError, match=r'Used file_prefix without diffs_path\.'):
        differ.compare(image1, image1, 'test_name')


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_writes_no_files_without_file_prefix(tmp_path):
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), (0, 255, 0, 255))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    diffs_path = tmp_path / 'image_diffs'
    differ = LiveImageDiffer(diffs_path)

    differ.compare(image1, image2)

    assert list(diffs_path.iterdir()) == []


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_two_sets(tmp_path):
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), (0, 0, 100, 255))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    diffs_path = tmp_path / 'image_diffs'
    actual_path1 = diffs_path / 'test_name-actual.png'
    actual_path2 = diffs_path / 'other_name-actual.png'
    differ = LiveImageDiffer(diffs_path)

    differ.compare(image1, image2, 'test_name')
    differ.compare(image1, image2, 'other_name')

    assert actual_path1.exists()
    assert actual_path2.exists()


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_compare_two_sizes():
    blue = (0, 0, 255, 255)
    green = (0, 255, 0, 255)
    missing_blue = (255, 255, 51, 255)
    missing_green = (255, 51, 0, 255)
    image1 = LivePillowImage(Image.new('RGBA', (2, 3)))
    image1.set_pixel((0, 2), blue)
    image2 = LivePillowImage(Image.new('RGBA', (3, 2)))
    image2.set_pixel((2, 0), green)

    differ = LiveImageDiffer()

    diff = differ.compare(image1, image2).convert_to_painter()

    diff_pixel1 = diff.get_pixel((0, 2))
    diff_pixel2 = diff.get_pixel((2, 0))

    assert diff_pixel1 == missing_blue
    assert diff_pixel2 == missing_green
    assert differ.diff_count == 5


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_remove_common_prefix(tmp_path):
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), (0, 0, 101, 255))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    diffs_path = tmp_path / 'image_diffs'
    actual_path1 = diffs_path / 'apple-actual.png'
    actual_path2 = diffs_path / 'banana-actual.png'
    differ = LiveImageDiffer(diffs_path)

    differ.compare(image1, image2, 'test_apple')
    differ.compare(image1, image2, 'test_banana')
    differ.remove_common_prefix()

    assert actual_path1.exists()
    assert actual_path2.exists()


# noinspection DuplicatedCode
@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_remove_no_prefix(tmp_path):
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image1.set_pixel((5, 10), (0, 0, 101, 255))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    diffs_path = tmp_path / 'image_diffs'
    actual_path1 = diffs_path / 'apple-actual.png'
    actual_path2 = diffs_path / 'banana-actual.png'
    differ = LiveImageDiffer(diffs_path)

    differ.compare(image1, image2, 'apple')
    differ.compare(image1, image2, 'banana')
    differ.remove_common_prefix()

    assert actual_path1.exists()
    assert actual_path2.exists()


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_cleans_diffs_path(tmp_path):
    diffs_path = tmp_path / 'image_diffs'
    diffs_path.mkdir()
    leftover_path = diffs_path / 'leftover-actual.png'
    leftover_path.write_text('garbage')
    unrelated_path = diffs_path / 'leftover-unrelated.png'
    unrelated_path.write_text('garbage')

    LiveImageDiffer(diffs_path)

    assert unrelated_path.exists()
    assert not leftover_path.exists()


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_duplicate_file_prefix(tmp_path):
    image = LivePillowImage(Image.new('RGBA', (10, 20)))
    differ = LiveImageDiffer(tmp_path)

    differ.compare(image, image, 'first_test')
    differ.compare(image, image, 'other_test')
    with pytest.raises(ValueError,
                       match=r"Duplicate file_prefix: 'first_test'\."):
        differ.compare(image, image, 'first_test')


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_assert_passes():
    image1 = LivePillowImage(Image.new('RGBA', (10, 20)))
    image2 = LivePillowImage(Image.new('RGBA', (10, 20)))

    differ = LiveImageDiffer()

    differ.assert_equal(image1, image2)


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_assert_fails():
    light_blue = (0, 0, 127, 255)
    blue = (0, 0, 255, 255)

    image1 = LivePillowImage(Image.new('RGBA', (10, 20), 'black'))
    image1.set_pixel((5, 10), light_blue)
    image2 = LivePillowImage(Image.new('RGBA', (10, 20), 'black'))

    differ = LiveImageDiffer()

    with pytest.raises(AssertionError, match=r'Images differ by 1 pixel with '
                                             r'a maximum difference of 127\.'):
        differ.assert_equal(image1, image2)

    image1.set_pixel((5, 11), blue)

    with pytest.raises(AssertionError, match=r'Images differ by 2 pixels with '
                                             r'a maximum difference of 255\.'):
        differ.assert_equal(image1, image2)


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_create_painters_fails():
    differ = LiveImageDiffer()
    expected: LivePainter
    actual: LivePainter

    with pytest.raises(AssertionError, match=r'Images differ by 1 pixel'):
        with differ.create_painters((100, 100)) as (expected, actual):
            expected.set_pixel((50, 50), (255, 255, 255, 255))


@pytest.mark.skipif(Image is None, reason='Pillow not installed.')
def test_differ_create_painters_error(patched_turtle):
    assert patched_turtle

    t = MockTurtle()
    differ = LiveImageDiffer()

    with pytest.raises(ZeroDivisionError):
        with differ.create_painters((100, 100)):
            print('This will raise an error:', 1/0)

    report_lines = t.report
    assert report_lines[-1] == "    text='ZeroDivisionError: division by zero'"


@pytest.mark.skipif(Image is not None, reason='Pillow is installed.')
def test_differ_create_painters_without_pillow(patched_turtle):
    assert patched_turtle

    differ = LiveImageDiffer()

    expected_error = (r'Pillow is not installed\. Install it, or '
                      r'override LiveImageDiffer\.start_painter\(\)\.')
    with pytest.raises(RuntimeError, match=expected_error):
        with differ.create_painters((100, 100)):
            pass


@pytest.mark.skipif(Image is not None, reason='Pillow is installed.')
def test_convert_to_painter_without_pillow(patched_turtle):
    assert patched_turtle

    image_data = b'PNG_IMAGE_DATA'

    image = LivePng(image_data)

    expected_error = (r'Pillow is not installed\. Install it, or '
                      r'override LivePng\.convert_to_painter\(\)\.')
    with pytest.raises(RuntimeError, match=expected_error):
        image.convert_to_painter()
