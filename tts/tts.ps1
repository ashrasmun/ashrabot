Param(
    [Parameter(Position=0, mandatory=$true)]
    [string] $TextToSay
)

Function Main {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.Volume = 100
    $synth.Speak($TextToSay)
}

Main
