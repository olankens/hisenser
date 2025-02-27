# <samp>OVERVIEW</samp>

Reverse engineered MQTT client for Hisense TVs.

<table>
  <tr align="center">
    <th><samp>AND</samp></th>
    <th><samp>IOS</samp></th>
    <th><samp>LIN</samp></th>
    <th><samp>MAC</samp></th>
    <th><samp>WIN</samp></th>
    <th><samp>WEB</samp></th>
  </tr>
  <tr align="center" height="50">
    <td width="9999">🟥</td>
    <td width="9999">🟥</td>
    <td width="9999">🟩</td>
    <td width="9999">🟩</td>
    <td width="9999">🟩</td>
    <td width="9999">🟥</td>
  </tr>
</table>

# <samp>GUIDANCE</samp>

### Import the library

```shell
poetry add git+https://github.com/olankens/hisenser.git
```

### Change current picture mode

Sadly, there is no way to determine the current mode.

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
