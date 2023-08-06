__version__ = "0.6.0"

from wow_ai_cv.classification.core import Classifications
from wow_ai_cv.dataset.core import (
    BaseDataset,
    ClassificationDataset,
    DetectionDataset,
)
from wow_ai_cv.detection.annotate import BoxAnnotator, MaskAnnotator
from wow_ai_cv.detection.core import Detections
from wow_ai_cv.detection.line_counter import LineZone, LineZoneAnnotator
from wow_ai_cv.detection.tools.polygon_zone import PolygonZone, PolygonZoneAnnotator
from wow_ai_cv.detection.utils import (
    box_iou_batch,
    filter_polygons_by_area,
    mask_to_polygons,
    mask_to_xyxy,
    non_max_suppression,
    polygon_to_mask,
    polygon_to_xyxy,
)
from wow_ai_cv.draw.color import Color, ColorPalette
from wow_ai_cv.draw.utils import draw_filled_rectangle, draw_polygon, draw_text
from wow_ai_cv.geometry.core import Point, Position, Rect
from wow_ai_cv.geometry.utils import get_polygon_center
from wow_ai_cv.utils.file import list_files_with_extensions
from wow_ai_cv.utils.image import ImageSink, crop
from wow_ai_cv.utils.notebook import plot_image, plot_images_grid
from wow_ai_cv.utils.video import (
    VideoInfo,
    VideoSink,
    get_video_frames_generator,
    process_video,
)
