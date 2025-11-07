<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".assets/icon-dark.png">
    <img src=".assets/icon-light.png" width="144">
  </picture>
</p>

<h1 align="center"><samp>HISENSER</samp></h1>

<p align="center">Reverse engineered MQTT client for Hisense TVs that helps you automatically set up picture profiles (SDR, HDR10, HDR+, and DOVI) after each firmware upgrade. This library uses a dummy certificate and private key to bypass broker authentication. Some TV models may require OTP-based permission.</p>

<hr>

<h3 align="center">Import Library</h3>

```shell
poetry add git+https://github.com/olankens/hisenser.git

```

<hr>

<h3 align="center">Change Current Mode</h3>

```python
with (client := Client(input("enter television ip address: ").strip(), foolish=True, secured=True)):
    if not client.attach():
        client.permit(input("enter television pairing code: ").strip())
    client.change_picture_mode(PictureMode.CINEMA_NIGHT)
    client.revert_picture_mode()
    client.change_apply_picture(ApplyPicture.ALL)
    client.change_local_dimming(LocalDimming.MEDIUM)
    client.change_backlight(40)
    client.change_brightness(50)
    client.change_contrast(75)
    client.change_color_saturation(50)
    client.change_sharpness(10)
    client.change_adaptive_contrast(AdaptiveContrast.OFF)
    client.change_ultra_smooth_motion(UltraSmoothMotion.OFF)
    client.change_noise_reduction(NoiseReduction.OFF)
    client.change_color_temperature(ColorTemperature.WARM1)
    client.change_color_gamut(ColorGamut.NATIVE)
    client.change_gamma_adjustment(GammaAdjustment.GAMMA_2_2)
    client.toggle_viewing_angle()
```
