# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PresetArgs', 'Preset']

@pulumi.input_type
class PresetArgs:
    def __init__(__self__, *,
                 container: pulumi.Input[str],
                 audio: Optional[pulumi.Input['PresetAudioArgs']] = None,
                 audio_codec_options: Optional[pulumi.Input['PresetAudioCodecOptionsArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 thumbnails: Optional[pulumi.Input['PresetThumbnailsArgs']] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 video: Optional[pulumi.Input['PresetVideoArgs']] = None,
                 video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]]] = None):
        """
        The set of arguments for constructing a Preset resource.
        :param pulumi.Input[str] container: The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        :param pulumi.Input['PresetAudioArgs'] audio: Audio parameters object (documented below).
        :param pulumi.Input['PresetAudioCodecOptionsArgs'] audio_codec_options: Codec options for the audio parameters (documented below)
        :param pulumi.Input[str] description: A description of the preset (maximum 255 characters)
        :param pulumi.Input[str] name: The name of the preset. (maximum 40 characters)
        :param pulumi.Input['PresetThumbnailsArgs'] thumbnails: Thumbnail parameters object (documented below)
        :param pulumi.Input['PresetVideoArgs'] video: Video parameters object (documented below)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] video_codec_options: Codec options for the video parameters
        :param pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]] video_watermarks: Watermark parameters for the video parameters (documented below)
        """
        pulumi.set(__self__, "container", container)
        if audio is not None:
            pulumi.set(__self__, "audio", audio)
        if audio_codec_options is not None:
            pulumi.set(__self__, "audio_codec_options", audio_codec_options)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if thumbnails is not None:
            pulumi.set(__self__, "thumbnails", thumbnails)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if video is not None:
            pulumi.set(__self__, "video", video)
        if video_codec_options is not None:
            pulumi.set(__self__, "video_codec_options", video_codec_options)
        if video_watermarks is not None:
            pulumi.set(__self__, "video_watermarks", video_watermarks)

    @property
    @pulumi.getter
    def container(self) -> pulumi.Input[str]:
        """
        The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        """
        return pulumi.get(self, "container")

    @container.setter
    def container(self, value: pulumi.Input[str]):
        pulumi.set(self, "container", value)

    @property
    @pulumi.getter
    def audio(self) -> Optional[pulumi.Input['PresetAudioArgs']]:
        """
        Audio parameters object (documented below).
        """
        return pulumi.get(self, "audio")

    @audio.setter
    def audio(self, value: Optional[pulumi.Input['PresetAudioArgs']]):
        pulumi.set(self, "audio", value)

    @property
    @pulumi.getter(name="audioCodecOptions")
    def audio_codec_options(self) -> Optional[pulumi.Input['PresetAudioCodecOptionsArgs']]:
        """
        Codec options for the audio parameters (documented below)
        """
        return pulumi.get(self, "audio_codec_options")

    @audio_codec_options.setter
    def audio_codec_options(self, value: Optional[pulumi.Input['PresetAudioCodecOptionsArgs']]):
        pulumi.set(self, "audio_codec_options", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the preset (maximum 255 characters)
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the preset. (maximum 40 characters)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def thumbnails(self) -> Optional[pulumi.Input['PresetThumbnailsArgs']]:
        """
        Thumbnail parameters object (documented below)
        """
        return pulumi.get(self, "thumbnails")

    @thumbnails.setter
    def thumbnails(self, value: Optional[pulumi.Input['PresetThumbnailsArgs']]):
        pulumi.set(self, "thumbnails", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def video(self) -> Optional[pulumi.Input['PresetVideoArgs']]:
        """
        Video parameters object (documented below)
        """
        return pulumi.get(self, "video")

    @video.setter
    def video(self, value: Optional[pulumi.Input['PresetVideoArgs']]):
        pulumi.set(self, "video", value)

    @property
    @pulumi.getter(name="videoCodecOptions")
    def video_codec_options(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Codec options for the video parameters
        """
        return pulumi.get(self, "video_codec_options")

    @video_codec_options.setter
    def video_codec_options(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "video_codec_options", value)

    @property
    @pulumi.getter(name="videoWatermarks")
    def video_watermarks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]]]:
        """
        Watermark parameters for the video parameters (documented below)
        """
        return pulumi.get(self, "video_watermarks")

    @video_watermarks.setter
    def video_watermarks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]]]):
        pulumi.set(self, "video_watermarks", value)


@pulumi.input_type
class _PresetState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 audio: Optional[pulumi.Input['PresetAudioArgs']] = None,
                 audio_codec_options: Optional[pulumi.Input['PresetAudioCodecOptionsArgs']] = None,
                 container: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 thumbnails: Optional[pulumi.Input['PresetThumbnailsArgs']] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 video: Optional[pulumi.Input['PresetVideoArgs']] = None,
                 video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]]] = None):
        """
        Input properties used for looking up and filtering Preset resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the Elastic Transcoder Preset.
        :param pulumi.Input['PresetAudioArgs'] audio: Audio parameters object (documented below).
        :param pulumi.Input['PresetAudioCodecOptionsArgs'] audio_codec_options: Codec options for the audio parameters (documented below)
        :param pulumi.Input[str] container: The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        :param pulumi.Input[str] description: A description of the preset (maximum 255 characters)
        :param pulumi.Input[str] name: The name of the preset. (maximum 40 characters)
        :param pulumi.Input['PresetThumbnailsArgs'] thumbnails: Thumbnail parameters object (documented below)
        :param pulumi.Input['PresetVideoArgs'] video: Video parameters object (documented below)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] video_codec_options: Codec options for the video parameters
        :param pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]] video_watermarks: Watermark parameters for the video parameters (documented below)
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if audio is not None:
            pulumi.set(__self__, "audio", audio)
        if audio_codec_options is not None:
            pulumi.set(__self__, "audio_codec_options", audio_codec_options)
        if container is not None:
            pulumi.set(__self__, "container", container)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if thumbnails is not None:
            pulumi.set(__self__, "thumbnails", thumbnails)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if video is not None:
            pulumi.set(__self__, "video", video)
        if video_codec_options is not None:
            pulumi.set(__self__, "video_codec_options", video_codec_options)
        if video_watermarks is not None:
            pulumi.set(__self__, "video_watermarks", video_watermarks)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the Elastic Transcoder Preset.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def audio(self) -> Optional[pulumi.Input['PresetAudioArgs']]:
        """
        Audio parameters object (documented below).
        """
        return pulumi.get(self, "audio")

    @audio.setter
    def audio(self, value: Optional[pulumi.Input['PresetAudioArgs']]):
        pulumi.set(self, "audio", value)

    @property
    @pulumi.getter(name="audioCodecOptions")
    def audio_codec_options(self) -> Optional[pulumi.Input['PresetAudioCodecOptionsArgs']]:
        """
        Codec options for the audio parameters (documented below)
        """
        return pulumi.get(self, "audio_codec_options")

    @audio_codec_options.setter
    def audio_codec_options(self, value: Optional[pulumi.Input['PresetAudioCodecOptionsArgs']]):
        pulumi.set(self, "audio_codec_options", value)

    @property
    @pulumi.getter
    def container(self) -> Optional[pulumi.Input[str]]:
        """
        The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        """
        return pulumi.get(self, "container")

    @container.setter
    def container(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the preset (maximum 255 characters)
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the preset. (maximum 40 characters)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def thumbnails(self) -> Optional[pulumi.Input['PresetThumbnailsArgs']]:
        """
        Thumbnail parameters object (documented below)
        """
        return pulumi.get(self, "thumbnails")

    @thumbnails.setter
    def thumbnails(self, value: Optional[pulumi.Input['PresetThumbnailsArgs']]):
        pulumi.set(self, "thumbnails", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def video(self) -> Optional[pulumi.Input['PresetVideoArgs']]:
        """
        Video parameters object (documented below)
        """
        return pulumi.get(self, "video")

    @video.setter
    def video(self, value: Optional[pulumi.Input['PresetVideoArgs']]):
        pulumi.set(self, "video", value)

    @property
    @pulumi.getter(name="videoCodecOptions")
    def video_codec_options(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Codec options for the video parameters
        """
        return pulumi.get(self, "video_codec_options")

    @video_codec_options.setter
    def video_codec_options(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "video_codec_options", value)

    @property
    @pulumi.getter(name="videoWatermarks")
    def video_watermarks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]]]:
        """
        Watermark parameters for the video parameters (documented below)
        """
        return pulumi.get(self, "video_watermarks")

    @video_watermarks.setter
    def video_watermarks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PresetVideoWatermarkArgs']]]]):
        pulumi.set(self, "video_watermarks", value)


class Preset(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audio: Optional[pulumi.Input[pulumi.InputType['PresetAudioArgs']]] = None,
                 audio_codec_options: Optional[pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']]] = None,
                 container: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 thumbnails: Optional[pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 video: Optional[pulumi.Input[pulumi.InputType['PresetVideoArgs']]] = None,
                 video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]]] = None,
                 __props__=None):
        """
        Provides an Elastic Transcoder preset resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        bar = aws.elastictranscoder.Preset("bar",
            audio=aws.elastictranscoder.PresetAudioArgs(
                audio_packing_mode="SingleTrack",
                bit_rate="96",
                channels="2",
                codec="AAC",
                sample_rate="44100",
            ),
            audio_codec_options=aws.elastictranscoder.PresetAudioCodecOptionsArgs(
                profile="AAC-LC",
            ),
            container="mp4",
            description="Sample Preset",
            thumbnails=aws.elastictranscoder.PresetThumbnailsArgs(
                format="png",
                interval="120",
                max_height="auto",
                max_width="auto",
                padding_policy="Pad",
                sizing_policy="Fit",
            ),
            video=aws.elastictranscoder.PresetVideoArgs(
                bit_rate="1600",
                codec="H.264",
                display_aspect_ratio="16:9",
                fixed_gop="false",
                frame_rate="auto",
                keyframes_max_dist="240",
                max_frame_rate="60",
                max_height="auto",
                max_width="auto",
                padding_policy="Pad",
                sizing_policy="Fit",
            ),
            video_codec_options={
                "ColorSpaceConversionMode": "None",
                "InterlacedMode": "Progressive",
                "Level": "2.2",
                "MaxReferenceFrames": "3",
                "Profile": "main",
            },
            video_watermarks=[aws.elastictranscoder.PresetVideoWatermarkArgs(
                horizontal_align="Right",
                horizontal_offset="10px",
                id="Test",
                max_height="20%",
                max_width="20%",
                opacity="55.5",
                sizing_policy="ShrinkToFit",
                target="Content",
                vertical_align="Bottom",
                vertical_offset="10px",
            )])
        ```

        ## Import

        Elastic Transcoder presets can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:elastictranscoder/preset:Preset basic_preset 1407981661351-cttk8b
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PresetAudioArgs']] audio: Audio parameters object (documented below).
        :param pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']] audio_codec_options: Codec options for the audio parameters (documented below)
        :param pulumi.Input[str] container: The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        :param pulumi.Input[str] description: A description of the preset (maximum 255 characters)
        :param pulumi.Input[str] name: The name of the preset. (maximum 40 characters)
        :param pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']] thumbnails: Thumbnail parameters object (documented below)
        :param pulumi.Input[pulumi.InputType['PresetVideoArgs']] video: Video parameters object (documented below)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] video_codec_options: Codec options for the video parameters
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]] video_watermarks: Watermark parameters for the video parameters (documented below)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PresetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Elastic Transcoder preset resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        bar = aws.elastictranscoder.Preset("bar",
            audio=aws.elastictranscoder.PresetAudioArgs(
                audio_packing_mode="SingleTrack",
                bit_rate="96",
                channels="2",
                codec="AAC",
                sample_rate="44100",
            ),
            audio_codec_options=aws.elastictranscoder.PresetAudioCodecOptionsArgs(
                profile="AAC-LC",
            ),
            container="mp4",
            description="Sample Preset",
            thumbnails=aws.elastictranscoder.PresetThumbnailsArgs(
                format="png",
                interval="120",
                max_height="auto",
                max_width="auto",
                padding_policy="Pad",
                sizing_policy="Fit",
            ),
            video=aws.elastictranscoder.PresetVideoArgs(
                bit_rate="1600",
                codec="H.264",
                display_aspect_ratio="16:9",
                fixed_gop="false",
                frame_rate="auto",
                keyframes_max_dist="240",
                max_frame_rate="60",
                max_height="auto",
                max_width="auto",
                padding_policy="Pad",
                sizing_policy="Fit",
            ),
            video_codec_options={
                "ColorSpaceConversionMode": "None",
                "InterlacedMode": "Progressive",
                "Level": "2.2",
                "MaxReferenceFrames": "3",
                "Profile": "main",
            },
            video_watermarks=[aws.elastictranscoder.PresetVideoWatermarkArgs(
                horizontal_align="Right",
                horizontal_offset="10px",
                id="Test",
                max_height="20%",
                max_width="20%",
                opacity="55.5",
                sizing_policy="ShrinkToFit",
                target="Content",
                vertical_align="Bottom",
                vertical_offset="10px",
            )])
        ```

        ## Import

        Elastic Transcoder presets can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:elastictranscoder/preset:Preset basic_preset 1407981661351-cttk8b
        ```

        :param str resource_name: The name of the resource.
        :param PresetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PresetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audio: Optional[pulumi.Input[pulumi.InputType['PresetAudioArgs']]] = None,
                 audio_codec_options: Optional[pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']]] = None,
                 container: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 thumbnails: Optional[pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 video: Optional[pulumi.Input[pulumi.InputType['PresetVideoArgs']]] = None,
                 video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PresetArgs.__new__(PresetArgs)

            __props__.__dict__["audio"] = audio
            __props__.__dict__["audio_codec_options"] = audio_codec_options
            if container is None and not opts.urn:
                raise TypeError("Missing required property 'container'")
            __props__.__dict__["container"] = container
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["thumbnails"] = thumbnails
            __props__.__dict__["type"] = type
            __props__.__dict__["video"] = video
            __props__.__dict__["video_codec_options"] = video_codec_options
            __props__.__dict__["video_watermarks"] = video_watermarks
            __props__.__dict__["arn"] = None
        super(Preset, __self__).__init__(
            'aws:elastictranscoder/preset:Preset',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            audio: Optional[pulumi.Input[pulumi.InputType['PresetAudioArgs']]] = None,
            audio_codec_options: Optional[pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']]] = None,
            container: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            thumbnails: Optional[pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']]] = None,
            type: Optional[pulumi.Input[str]] = None,
            video: Optional[pulumi.Input[pulumi.InputType['PresetVideoArgs']]] = None,
            video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]]] = None) -> 'Preset':
        """
        Get an existing Preset resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the Elastic Transcoder Preset.
        :param pulumi.Input[pulumi.InputType['PresetAudioArgs']] audio: Audio parameters object (documented below).
        :param pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']] audio_codec_options: Codec options for the audio parameters (documented below)
        :param pulumi.Input[str] container: The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        :param pulumi.Input[str] description: A description of the preset (maximum 255 characters)
        :param pulumi.Input[str] name: The name of the preset. (maximum 40 characters)
        :param pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']] thumbnails: Thumbnail parameters object (documented below)
        :param pulumi.Input[pulumi.InputType['PresetVideoArgs']] video: Video parameters object (documented below)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] video_codec_options: Codec options for the video parameters
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]] video_watermarks: Watermark parameters for the video parameters (documented below)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PresetState.__new__(_PresetState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["audio"] = audio
        __props__.__dict__["audio_codec_options"] = audio_codec_options
        __props__.__dict__["container"] = container
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["thumbnails"] = thumbnails
        __props__.__dict__["type"] = type
        __props__.__dict__["video"] = video
        __props__.__dict__["video_codec_options"] = video_codec_options
        __props__.__dict__["video_watermarks"] = video_watermarks
        return Preset(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the Elastic Transcoder Preset.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def audio(self) -> pulumi.Output[Optional['outputs.PresetAudio']]:
        """
        Audio parameters object (documented below).
        """
        return pulumi.get(self, "audio")

    @property
    @pulumi.getter(name="audioCodecOptions")
    def audio_codec_options(self) -> pulumi.Output['outputs.PresetAudioCodecOptions']:
        """
        Codec options for the audio parameters (documented below)
        """
        return pulumi.get(self, "audio_codec_options")

    @property
    @pulumi.getter
    def container(self) -> pulumi.Output[str]:
        """
        The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        """
        return pulumi.get(self, "container")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the preset (maximum 255 characters)
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the preset. (maximum 40 characters)
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def thumbnails(self) -> pulumi.Output[Optional['outputs.PresetThumbnails']]:
        """
        Thumbnail parameters object (documented below)
        """
        return pulumi.get(self, "thumbnails")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def video(self) -> pulumi.Output[Optional['outputs.PresetVideo']]:
        """
        Video parameters object (documented below)
        """
        return pulumi.get(self, "video")

    @property
    @pulumi.getter(name="videoCodecOptions")
    def video_codec_options(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Codec options for the video parameters
        """
        return pulumi.get(self, "video_codec_options")

    @property
    @pulumi.getter(name="videoWatermarks")
    def video_watermarks(self) -> pulumi.Output[Optional[Sequence['outputs.PresetVideoWatermark']]]:
        """
        Watermark parameters for the video parameters (documented below)
        """
        return pulumi.get(self, "video_watermarks")

