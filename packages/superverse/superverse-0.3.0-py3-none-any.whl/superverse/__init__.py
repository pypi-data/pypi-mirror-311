import importlib.metadata as importlib_metadata

try:
    # This will read version from pyproject.toml
    __version__ = importlib_metadata.version(__package__ or __name__)
except importlib_metadata.PackageNotFoundError:
    __version__ = "development"

from superverse.annotators.core import (
    BackgroundOverlayAnnotator,
    BlurAnnotator,
    BoundingBoxAnnotator,
    BoxAnnotator,
    BoxCornerAnnotator,
    CircleAnnotator,
    ColorAnnotator,
    CropAnnotator,
    DotAnnotator,
    EllipseAnnotator,
    HaloAnnotator,
    HeatMapAnnotator,
    IconAnnotator,
    LabelAnnotator,
    MaskAnnotator,
    OrientedBoxAnnotator,
    PercentageBarAnnotator,
    PixelateAnnotator,
    PolygonAnnotator,
    RichLabelAnnotator,
    RoundBoxAnnotator,
    TraceAnnotator,
    TriangleAnnotator,
)
from superverse.annotators.utils import ColorLookup
from superverse.classification.core import Classifications
from superverse.dataset.core import (
    BaseDataset,
    ClassificationDataset,
    DetectionDataset,
)
from superverse.dataset.utils import mask_to_rle, rle_to_mask
from superverse.detection.core import Detections
from superverse.detection.line_zone import (
    LineZone,
    LineZoneAnnotator,
    LineZoneAnnotatorMulticlass,
)
from superverse.detection.lmm import LMM
from superverse.detection.overlap_filter import (
    OverlapFilter,
    box_non_max_merge,
    box_non_max_suppression,
    mask_non_max_suppression,
)
from superverse.detection.tools.csv_sink import CSVSink
from superverse.detection.tools.inference_slicer import InferenceSlicer
from superverse.detection.tools.json_sink import JSONSink
from superverse.detection.tools.polygon_zone import PolygonZone, PolygonZoneAnnotator
from superverse.detection.tools.smoother import DetectionsSmoother
from superverse.detection.utils import (
    box_iou_batch,
    calculate_masks_centroids,
    clip_boxes,
    contains_holes,
    contains_multiple_segments,
    filter_polygons_by_area,
    mask_iou_batch,
    mask_to_polygons,
    mask_to_xyxy,
    move_boxes,
    move_masks,
    oriented_box_iou_batch,
    pad_boxes,
    polygon_to_mask,
    polygon_to_xyxy,
    scale_boxes,
    xcycwh_to_xyxy,
    xywh_to_xyxy,
)
from superverse.draw.color import Color, ColorPalette
from superverse.draw.utils import (
    calculate_optimal_line_thickness,
    calculate_optimal_text_scale,
    draw_filled_polygon,
    draw_filled_rectangle,
    draw_image,
    draw_line,
    draw_polygon,
    draw_rectangle,
    draw_text,
)
from superverse.geometry.core import Point, Position, Rect
from superverse.geometry.utils import get_polygon_center
from superverse.keypoint.annotators import (
    EdgeAnnotator,
    VertexAnnotator,
    VertexLabelAnnotator,
)
from superverse.keypoint.core import KeyPoints
from superverse.metrics.detection import ConfusionMatrix, MeanAveragePrecision
from superverse.tracker.byte_tracker.core import ByteTrack
from superverse.utils.conversion import cv2_to_pillow, pillow_to_cv2
from superverse.utils.file import list_files_with_extensions
from superverse.utils.image import (
    ImageSink,
    create_tiles,
    crop_image,
    letterbox_image,
    overlay_image,
    resize_image,
    scale_image,
)
from superverse.utils.notebook import plot_image, plot_images_grid
from superverse.utils.video import (
    FPSMonitor,
    VideoInfo,
    VideoSink,
    get_video_frames_generator,
    process_video,
)
