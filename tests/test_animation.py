"""Tests for shape animation: timeline, sequences, effects, timing, behaviors, motion paths."""
import os
import tempfile
import pytest
from aspose.slides_foss import Presentation, ShapeType, Paragraph
from aspose.slides_foss import animation as anim
from aspose.slides_foss.export import SaveFormat


# ---------------------------------------------------------------------------
# Timeline access
# ---------------------------------------------------------------------------

class TestTimeline:
    """BaseSlide.timeline returns an AnimationTimeLine."""

    def test_timeline_not_none(self):
        with Presentation() as pres:
            tl = pres.slides[0].timeline
            assert tl is not None

    def test_main_sequence_not_none(self):
        with Presentation() as pres:
            seq = pres.slides[0].timeline.main_sequence
            assert seq is not None

    def test_main_sequence_initially_empty(self):
        with Presentation() as pres:
            assert pres.slides[0].timeline.main_sequence.count == 0

    def test_interactive_sequences_initially_empty(self):
        with Presentation() as pres:
            assert len(pres.slides[0].timeline.interactive_sequences) == 0


# ---------------------------------------------------------------------------
# Adding effects
# ---------------------------------------------------------------------------

class TestAddEffect:
    """Sequence.add_effect creates effects with correct attributes."""

    def test_add_fade_effect(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence

            effect = seq.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )

            assert effect is not None
            assert effect.type == anim.EffectType.FADE
            assert effect.subtype == anim.EffectSubtype.NONE
            assert effect.preset_class_type == anim.EffectPresetClassType.ENTRANCE
            assert seq.count == 1

    def test_add_fly_effect_with_subtype(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence

            effect = seq.add_effect(
                shape, anim.EffectType.FLY,
                anim.EffectSubtype.LEFT,
                anim.EffectTriggerType.ON_CLICK,
            )

            assert effect.type == anim.EffectType.FLY
            assert effect.subtype == anim.EffectSubtype.LEFT

    def test_add_multiple_effects(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            s1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            s2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 200, 10, 100, 50)
            seq = slide.timeline.main_sequence

            seq.add_effect(s1, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(s2, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.AFTER_PREVIOUS)

            assert seq.count == 2

    def test_add_effect_target_shape(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )

            assert effect.target_shape is shape

    def test_add_path_effect(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.PATH_FOOTBALL,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )

            assert effect.type == anim.EffectType.PATH_FOOTBALL
            assert effect.preset_class_type == anim.EffectPresetClassType.PATH


# ---------------------------------------------------------------------------
# Effect round-trip (save / reload)
# ---------------------------------------------------------------------------

class TestEffectRoundTrip:
    """Effects survive save/reload cycle."""

    def test_fade_persists(self, tmp_pptx):
        pres = Presentation()
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
        slide.timeline.main_sequence.add_effect(
            shape, anim.EffectType.FADE,
            anim.EffectSubtype.NONE,
            anim.EffectTriggerType.ON_CLICK,
        )

        pres2 = tmp_pptx(pres)
        seq2 = pres2.slides[0].timeline.main_sequence
        assert seq2.count == 1
        assert seq2[0].type == anim.EffectType.FADE
        assert seq2[0].subtype == anim.EffectSubtype.NONE
        assert seq2[0].preset_class_type == anim.EffectPresetClassType.ENTRANCE
        pres2.dispose()

    def test_multiple_effects_persist(self, tmp_pptx):
        pres = Presentation()
        slide = pres.slides[0]
        s1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
        s2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 200, 10, 100, 50)
        seq = slide.timeline.main_sequence
        seq.add_effect(s1, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                       anim.EffectTriggerType.ON_CLICK)
        seq.add_effect(s2, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                       anim.EffectTriggerType.AFTER_PREVIOUS)

        pres2 = tmp_pptx(pres)
        seq2 = pres2.slides[0].timeline.main_sequence
        assert seq2.count == 2
        assert seq2[0].type == anim.EffectType.FADE
        assert seq2[1].type == anim.EffectType.APPEAR
        pres2.dispose()

    def test_no_animation_slide_has_zero_effects(self, tmp_pptx):
        """A slide without animations should have an empty sequence on reload."""
        pres = Presentation()
        pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 50, 50)

        pres2 = tmp_pptx(pres)
        assert pres2.slides[0].timeline.main_sequence.count == 0
        pres2.dispose()


# ---------------------------------------------------------------------------
# Timing properties
# ---------------------------------------------------------------------------

class TestTiming:
    """Effect.timing read/write properties."""

    def test_default_trigger_type(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            assert effect.timing.trigger_type == anim.EffectTriggerType.ON_CLICK

    def test_set_duration(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            effect.timing.duration = 3.0
            assert effect.timing.duration == 3.0

    def test_set_trigger_delay(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            effect.timing.trigger_delay_time = 0.5
            assert effect.timing.trigger_delay_time == 0.5

    def test_timing_persists(self, tmp_pptx):
        pres = Presentation()
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
        effect = slide.timeline.main_sequence.add_effect(
            shape, anim.EffectType.FADE,
            anim.EffectSubtype.NONE,
            anim.EffectTriggerType.ON_CLICK,
        )
        effect.timing.duration = 2.5
        effect.timing.trigger_delay_time = 0.5

        pres2 = tmp_pptx(pres)
        eff2 = pres2.slides[0].timeline.main_sequence[0]
        assert eff2.timing.duration == 2.5
        assert eff2.timing.trigger_delay_time == 0.5
        pres2.dispose()

    def test_set_trigger_type(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            effect.timing.trigger_type = anim.EffectTriggerType.WITH_PREVIOUS
            assert effect.timing.trigger_type == anim.EffectTriggerType.WITH_PREVIOUS


# ---------------------------------------------------------------------------
# Behaviors
# ---------------------------------------------------------------------------

class TestBehaviors:
    """Effect.behaviors collection."""

    def test_entrance_effect_has_set_behavior(self):
        """Entrance effects get a default <p:set> visibility behavior."""
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            assert effect.behaviors.count >= 1
            assert isinstance(effect.behaviors[0], anim.SetEffect)

    def test_path_effect_has_motion_behavior(self):
        """Path effects get a default <p:animMotion> behavior."""
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.PATH_FOOTBALL,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            assert effect.behaviors.count >= 1
            assert isinstance(effect.behaviors[0], anim.MotionEffect)

    def test_behaviors_iterable(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            items = list(effect.behaviors)
            assert len(items) == effect.behaviors.count


# ---------------------------------------------------------------------------
# Interactive sequences
# ---------------------------------------------------------------------------

class TestInteractiveSequences:
    """SequenceCollection for interactive (click-on-shape) sequences."""

    def test_add_interactive_sequence(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            trigger = slide.shapes.add_auto_shape(ShapeType.BEVEL, 10, 10, 20, 20)
            target = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)

            seq = slide.timeline.interactive_sequences.add(trigger)
            assert seq is not None
            assert len(slide.timeline.interactive_sequences) == 1

    def test_interactive_sequence_add_effect(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            trigger = slide.shapes.add_auto_shape(ShapeType.BEVEL, 10, 10, 20, 20)
            target = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)

            seq = slide.timeline.interactive_sequences.add(trigger)
            effect = seq.add_effect(
                target, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            assert seq.count == 1
            assert effect.type == anim.EffectType.FADE

    def test_interactive_sequence_persists(self, tmp_pptx):
        pres = Presentation()
        slide = pres.slides[0]
        trigger = slide.shapes.add_auto_shape(ShapeType.BEVEL, 10, 10, 20, 20)
        target = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)

        seq = slide.timeline.interactive_sequences.add(trigger)
        seq.add_effect(target, anim.EffectType.FADE,
                       anim.EffectSubtype.NONE,
                       anim.EffectTriggerType.ON_CLICK)

        pres2 = tmp_pptx(pres)
        iseqs = pres2.slides[0].timeline.interactive_sequences
        assert len(iseqs) == 1
        assert iseqs[0].count == 1
        assert iseqs[0][0].type == anim.EffectType.FADE
        pres2.dispose()


# ---------------------------------------------------------------------------
# Motion paths
# ---------------------------------------------------------------------------

class TestMotionPath:
    """MotionEffect.path and MotionCmdPath."""

    def test_user_path_commands(self):
        from aspose.slides_foss.drawing import PointF

        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
            seq = slide.timeline.interactive_sequences.add(
                slide.shapes.add_auto_shape(ShapeType.BEVEL, 10, 10, 20, 20)
            )
            fx = seq.add_effect(shape, anim.EffectType.PATH_USER,
                                anim.EffectSubtype.NONE,
                                anim.EffectTriggerType.ON_CLICK)

            motion = fx.behaviors[0]
            assert isinstance(motion, anim.MotionEffect)

            pts1 = [PointF(0.076, 0.59)]
            motion.path.add(anim.MotionCommandPathType.LINE_TO, pts1,
                            anim.MotionPathPointsType.AUTO, True)
            pts2 = [PointF(-0.076, -0.59)]
            motion.path.add(anim.MotionCommandPathType.LINE_TO, pts2,
                            anim.MotionPathPointsType.AUTO, False)
            motion.path.add(anim.MotionCommandPathType.END, None,
                            anim.MotionPathPointsType.AUTO, False)

            assert motion.path.count == 3
            assert motion.path[0].command_type == anim.MotionCommandPathType.LINE_TO
            assert motion.path[0].is_relative is True
            assert motion.path[2].command_type == anim.MotionCommandPathType.END

    def test_motion_path_clear(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.interactive_sequences.add(
                slide.shapes.add_auto_shape(ShapeType.BEVEL, 10, 10, 20, 20)
            )
            fx = seq.add_effect(shape, anim.EffectType.PATH_USER,
                                anim.EffectSubtype.NONE,
                                anim.EffectTriggerType.ON_CLICK)
            motion = fx.behaviors[0]
            motion.path.add(anim.MotionCommandPathType.LINE_TO, [],
                            anim.MotionPathPointsType.AUTO, True)
            assert motion.path.count == 1
            motion.path.clear()
            assert motion.path.count == 0


# ---------------------------------------------------------------------------
# get_effects_by_shape / remove
# ---------------------------------------------------------------------------

class TestSequenceQueries:
    """Sequence query and mutation methods."""

    def test_get_effects_by_shape(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            s1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            s2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 200, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(s1, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(s2, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(s1, anim.EffectType.FLY, anim.EffectSubtype.LEFT,
                           anim.EffectTriggerType.AFTER_PREVIOUS)

            effs = seq.get_effects_by_shape(s1)
            assert len(effs) == 2
            effs2 = seq.get_effects_by_shape(s2)
            assert len(effs2) == 1

    def test_get_count_by_shape(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(shape, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.AFTER_PREVIOUS)

            assert seq.get_count(shape) == 2

    def test_remove_effect(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            eff = seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                                 anim.EffectTriggerType.ON_CLICK)
            assert seq.count == 1
            seq.remove(eff)
            assert seq.count == 0

    def test_remove_at(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(shape, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.AFTER_PREVIOUS)
            seq.remove_at(0)
            assert seq.count == 1
            assert seq[0].type == anim.EffectType.APPEAR

    def test_remove_by_shape(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            s1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            s2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 200, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(s1, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(s2, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(s1, anim.EffectType.FLY, anim.EffectSubtype.LEFT,
                           anim.EffectTriggerType.AFTER_PREVIOUS)

            seq.remove_by_shape(s1)
            assert seq.count == 1
            assert seq[0].type == anim.EffectType.APPEAR

    def test_clear_sequence(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(shape, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.AFTER_PREVIOUS)
            seq.clear()
            assert seq.count == 0


# ---------------------------------------------------------------------------
# Sequence indexing / iteration
# ---------------------------------------------------------------------------

class TestSequenceIteration:
    """Sequence supports indexing and iteration."""

    def test_getitem(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            assert seq[0].type == anim.EffectType.FADE

    def test_iteration(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(shape, anim.EffectType.APPEAR, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.AFTER_PREVIOUS)
            types = [e.type for e in seq]
            assert types == [anim.EffectType.FADE, anim.EffectType.APPEAR]

    def test_len(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            seq = slide.timeline.main_sequence
            seq.add_effect(shape, anim.EffectType.FADE, anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)
            assert len(seq) == 1


# ---------------------------------------------------------------------------
# TextAnimation
# ---------------------------------------------------------------------------

class TestTextAnimation:
    """Effect.text_animation properties."""

    def test_default_build_type(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            assert effect.text_animation.build_type == anim.BuildType.AS_ONE_OBJECT

    def test_set_build_type(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 100, 50)
            effect = slide.timeline.main_sequence.add_effect(
                shape, anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )
            effect.text_animation.build_type = anim.BuildType.BY_LEVEL_PARAGRAPHS1
            assert effect.text_animation.build_type == anim.BuildType.BY_LEVEL_PARAGRAPHS1


# ---------------------------------------------------------------------------
# BehaviorProperty
# ---------------------------------------------------------------------------

class TestBehaviorProperty:
    """BehaviorProperty predefined properties and get_or_create_by_value."""

    def test_predefined_value(self):
        bp = anim.BehaviorProperty()
        assert bp.ppt_x.value == 'ppt_x'
        assert bp.ppt_x.is_custom is False

    def test_style_visibility(self):
        bp = anim.BehaviorProperty()
        assert bp.style_visibility.value == 'style.visibility'

    def test_all_extrusion_properties_exist(self):
        bp = anim.BehaviorProperty()
        assert bp.extrusion_on.value == 'extrusion.on'
        assert bp.extrusion_color_mode.value == 'extrusion.colormode'

    def test_get_or_create_by_value_predefined(self):
        bp = anim.BehaviorProperty()
        result = bp.get_or_create_by_value('ppt_x')
        assert result is bp.ppt_x

    def test_get_or_create_by_value_custom(self):
        bp = anim.BehaviorProperty()
        result = bp.get_or_create_by_value('my.custom.prop')
        assert result.value == 'my.custom.prop'
        assert result.is_custom is True

    def test_default_is_custom(self):
        bp = anim.BehaviorProperty()
        assert bp.is_custom is True
        assert bp.value == ''


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TestEnums:
    """Animation enum values are accessible."""

    def test_effect_type_values(self):
        assert anim.EffectType.APPEAR.value == 'Appear'
        assert anim.EffectType.FADE.value == 'Fade'
        assert anim.EffectType.FLY.value == 'Fly'
        assert anim.EffectType.PATH_USER.value == 'PathUser'

    def test_effect_subtype_values(self):
        assert anim.EffectSubtype.NONE.value == 'None'
        assert anim.EffectSubtype.LEFT.value == 'Left'
        assert anim.EffectSubtype.RIGHT.value == 'Right'

    def test_effect_trigger_type_values(self):
        assert anim.EffectTriggerType.ON_CLICK.value == 'OnClick'
        assert anim.EffectTriggerType.WITH_PREVIOUS.value == 'WithPrevious'
        assert anim.EffectTriggerType.AFTER_PREVIOUS.value == 'AfterPrevious'

    def test_effect_preset_class_type_values(self):
        assert anim.EffectPresetClassType.ENTRANCE.value == 'Entrance'
        assert anim.EffectPresetClassType.EXIT.value == 'Exit'
        assert anim.EffectPresetClassType.EMPHASIS.value == 'Emphasis'
        assert anim.EffectPresetClassType.PATH.value == 'Path'

    def test_build_type_values(self):
        assert anim.BuildType.AS_ONE_OBJECT.value == 'AsOneObject'
        assert anim.BuildType.BY_LEVEL_PARAGRAPHS1.value == 'ByLevelParagraphs1'

    def test_motion_command_path_type_values(self):
        assert anim.MotionCommandPathType.MOVE_TO.value == 'MoveTo'
        assert anim.MotionCommandPathType.LINE_TO.value == 'LineTo'
        assert anim.MotionCommandPathType.END.value == 'End'


# ---------------------------------------------------------------------------
# Paragraph-level animation
# ---------------------------------------------------------------------------

class TestParagraphAnimation:
    """Sequence.add_effect with Paragraph target and get_effects_by_paragraph."""

    def _make_shape_with_paragraphs(self, slide):
        """Create a shape with 3 paragraphs and return (shape, [p0, p1, p2])."""
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)
        tf = shape.text_frame
        tf.paragraphs[0].text = "First paragraph"
        p2 = Paragraph()
        p2.text = "Second paragraph"
        tf.paragraphs.add(p2)
        p3 = Paragraph()
        p3.text = "Third paragraph"
        tf.paragraphs.add(p3)
        paras = list(tf.paragraphs)
        return shape, paras

    def test_add_effect_paragraph_returns_effect(self):
        with Presentation() as pres:
            slide = pres.slides[0]
            shape, paras = self._make_shape_with_paragraphs(slide)
            seq = slide.timeline.main_sequence

            effect = seq.add_effect(
                paras[0], anim.EffectType.FLY,
                anim.EffectSubtype.LEFT,
                anim.EffectTriggerType.ON_CLICK,
            )
            assert effect is not None
            assert effect.type == anim.EffectType.FLY

    def test_add_effect_paragraph_targets_correct_paragraph(self):
        """The XML should contain <p:pRg st='N' end='N'> for the targeted paragraph."""
        with Presentation() as pres:
            slide = pres.slides[0]
            shape, paras = self._make_shape_with_paragraphs(slide)
            seq = slide.timeline.main_sequence

            # Animate second paragraph (index 1)
            seq.add_effect(
                paras[1], anim.EffectType.FADE,
                anim.EffectSubtype.NONE,
                anim.EffectTriggerType.ON_CLICK,
            )

            # Verify via get_effects_by_paragraph
            assert len(seq.get_effects_by_paragraph(paras[0])) == 0
            assert len(seq.get_effects_by_paragraph(paras[1])) == 1
            assert len(seq.get_effects_by_paragraph(paras[2])) == 0

    def test_add_effect_multiple_paragraphs(self):
        """Different paragraphs can each have their own animation."""
        with Presentation() as pres:
            slide = pres.slides[0]
            shape, paras = self._make_shape_with_paragraphs(slide)
            seq = slide.timeline.main_sequence

            seq.add_effect(paras[0], anim.EffectType.FLY,
                           anim.EffectSubtype.LEFT,
                           anim.EffectTriggerType.ON_CLICK)
            seq.add_effect(paras[2], anim.EffectType.FADE,
                           anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.AFTER_PREVIOUS)

            assert len(seq.get_effects_by_paragraph(paras[0])) == 1
            assert len(seq.get_effects_by_paragraph(paras[1])) == 0
            assert len(seq.get_effects_by_paragraph(paras[2])) == 1
            assert seq.count == 2

    def test_paragraph_animation_round_trip(self):
        """Paragraph animation survives save/load cycle."""
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "para_anim.pptx")

            # Create and save
            with Presentation() as pres:
                slide = pres.slides[0]
                shape, paras = self._make_shape_with_paragraphs(slide)
                seq = slide.timeline.main_sequence
                seq.add_effect(paras[0], anim.EffectType.FLY,
                               anim.EffectSubtype.LEFT,
                               anim.EffectTriggerType.ON_CLICK)
                pres.save(path, SaveFormat.PPTX)

            # Reload and verify
            with Presentation(path) as pres:
                slide = pres.slides[0]
                seq = slide.timeline.main_sequence
                assert seq.count == 1

                # Find the animated shape
                animated_shape = None
                for i in range(len(slide.shapes)):
                    s = slide.shapes[i]
                    if len(seq.get_effects_by_shape(s)) > 0:
                        animated_shape = s
                        break
                assert animated_shape is not None

                tf = animated_shape.text_frame
                p0 = tf.paragraphs[0]
                effs = seq.get_effects_by_paragraph(p0)
                assert len(effs) == 1
                assert effs[0].type == anim.EffectType.FLY

    def test_get_effects_by_paragraph_no_match(self):
        """Paragraphs without animation return empty list."""
        with Presentation() as pres:
            slide = pres.slides[0]
            shape, paras = self._make_shape_with_paragraphs(slide)
            seq = slide.timeline.main_sequence

            # Add shape-level animation (no paragraph targeting)
            seq.add_effect(shape, anim.EffectType.FADE,
                           anim.EffectSubtype.NONE,
                           anim.EffectTriggerType.ON_CLICK)

            # Shape-level effect should NOT match paragraph queries
            assert len(seq.get_effects_by_paragraph(paras[0])) == 0
            assert len(seq.get_effects_by_paragraph(paras[1])) == 0
