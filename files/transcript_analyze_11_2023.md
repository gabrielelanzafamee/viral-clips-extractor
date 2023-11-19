# Transcript Analyze

Now we should get more info about the transcript like
 1. the **type** of video
 2. the **context** of the video
 3. the **topic** of the video

After that we should **summarize** and **remove** the parts useless of the transcript
 1. remove the parts where the **speaker** is **not talking**
 2. remove the parts where the **speaker** is talking but is not saying **anything important**
 3. remove the parts where the **speaker** is talking but is saying something **not related** to the video

After all these considerations we can know create multiple prompt for different type of type, context and topic of the transcript and choose the correct duration and parts to extract


<br>

How to process a long transcript without loosing context and information?

1. We can try checking and remove parts in every 4000 tokens