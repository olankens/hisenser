<div align="center">
  <p><img src="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/logo-light.png" align="center" width="128"/></p>
  <h1>HISENSER</h1>
</div>

<table><tr><td align="center" width="9999">
  &nbsp;<p>
    Python library for Hisense U7QF TV that automates picture profile setup for SDR, HDR10, HDR+, and Dolby Vision via reverse engineered MQTT client with dummy certificate to bypass broker authentication.
  </p>&nbsp;
</td></tr></table>

<table><tr><td align="center" height="72" width="9999">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/mqtt-dark.png"><img src="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/mqtt-light.png" align="center" width="48"/></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/1x1-dark.png"><img src="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/1x1-light.png" align="center" height="48" width="1"/></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/python-dark.png"><img src="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/python-light.png" align="center" width="48"/></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/1x1-dark.png"><img src="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/1x1-light.png" align="center" height="48" width="1"/></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/pycharm-dark.png"><img src="https://github.com/olankens/hisenser/raw/HEAD/.github/assets/pycharm-light.png" align="center" width="48"/></picture>
</td></tr></table>

### Platform Support

<table>
  <tr>
    <th align="center" width="9999"><samp>AND</samp></th>
    <th align="center" width="9999"><samp>IOS</samp></th>
    <th align="center" width="9999"><samp>LIN</samp></th>
    <th align="center" width="9999"><samp>MAC</samp></th>
    <th align="center" width="9999"><samp>WIN</samp></th>
    <th align="center" width="9999"><samp>WEB</samp></th>
  </tr>
  <tr>
    <td align="center" height="50">🟥</td>
    <td align="center">🟥</td>
    <td align="center">🟩</td>
    <td align="center">🟩</td>
    <td align="center">🟩</td>
    <td align="center">🟥</td>
  </tr>
</table>

### Add PyPI Package

```shell
poetry add git+https://github.com/olankens/hisenser.git
```

### Modify Picture Mode

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