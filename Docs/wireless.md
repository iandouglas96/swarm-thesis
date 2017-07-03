# Wireless command documentation

## Command format
- Command structured as series of unsigned chars
  - Command (and args) a single char as defined by an enum (starting with 0x10)
  - Characters below 0x10 are reserved for special use
  - To drive straight forwards (drive is 0x08), then, would be `15 FF FF`

- Responses
  - Responses encode the original command.
  - 0x00 signals a response, followed by the original command and then the payload
  - Response to dump (0x10) would be `00 10 <data>`
  - 0x01 signals a status update, followed by the update type

## Command list
| Command                 | Type | Mode            | Description                                 |
|-------------------------|------|-----------------|---------------------------------------------|
| dump                    | get  | id or broadcast | Get robot configuration                     |
| set_id <id_num>         | set  | id              | Set robot's ID (0 to 255)                   |
| verbose on/off          | cmd  | id or broadcast | Tell robot to send constant status updates  |
| set_const <const> <val> | set  | id or broadcast | Set specified calibration constant to value |
| stop                    | cmd  | id or broadcast | Shut down motors                            |
| drive <r_spd> <l_spd>   | cmd  | id              | Manually set motor speeds                   |
| set_channel <channel>   | cmd  | id              | Set frequency beacon channel                |
| auto                    | cmd  | id              | Reset manual command overrides              |
