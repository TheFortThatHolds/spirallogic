@echo off
echo 🔮 SpiralLogic Language Test Suite
echo.

echo Testing Journaling Support Ritual...
python spirallogic_cli.py examples\journaling_support.sl --verbose
echo.
echo =====================================
echo.

echo Testing Crisis Response Ritual...
python spirallogic_cli.py examples\crisis_response.sl --verbose
echo.

echo Done! Check spirallogic_attestations.log for audit trail.
pause