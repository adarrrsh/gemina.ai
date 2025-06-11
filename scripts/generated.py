from manim import *

class ConceptScene(Scene):
    def construct(self):
        # Step 1: Display a title introducing the voiceover speaker
        title = Text("Welcome from Adesh Patapsing!", font_size=40)
        self.play(Write(title))
        self.wait(2)  # Pause to sync with narration

        # Step 2: Transition the title out and show Adesh's introduction text
        self.play(FadeOut(title))
        intro_text = Text("Hi, my name is Adesh Patapsing.", font_size=32)
        self.play(Write(intro_text))
        self.wait(2)  # Pause as Adesh introduces himself

        # Step 3: Transition to demonstrate "testing purposes" visually
        self.play(FadeOut(intro_text))
        
        test_purpose_text = Text("This is a test recording...", font_size=32)
        self.play(Write(test_purpose_text))
        
        self.wait(2)  # Wait so the audience comprehends the "testing" statement

        # Step 4: Add a Thank You message
        self.play(FadeOut(test_purpose_text))
        thank_you_text = Text("Thank you!", font_size=40, color=YELLOW)
        self.play(Write(thank_you_text))
        
        # Add a small flare with glowing effect for the thank you
        self.play(
            thank_you_text.animate.scale(1.2).set_color(RED),
            rate_func=there_and_back, run_time=2
        )
        self.wait(2) # Thank you Statement doesn