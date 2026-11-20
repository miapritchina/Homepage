# Pinned notes. Coordinates are fractions of the full image (x, y = top-left; w, h = size).
# Written by Claude after looking at each image; interpretations, not museum text.
N = {}
def n(i, intro, pins): N[i] = {'intro': intro, 'pins': [dict(zip(('x','y','w','h','title','text'), p)) for p in pins]}

n('cma135836', 'A tall Northern Song-style landscape in the manner of Juran: soft, rounded mountains built up from long, wet strokes, with a temple tucked into the trees. Zoom in to see how the mountain is made almost entirely of repeated brush marks.', [
 (.26,.335,.45,.10,'"Alum-head" boulders','The clustered round rocks along the summit, called "alum heads" (礬頭), are the signature motif of the Dong Yuan–Juran tradition.'),
 (.15,.40,.55,.16,'Hemp-fibre strokes','Long, slightly wavy parallel strokes (披麻皴) run down the mountain like loose fibres. They model the slopes without any hard outline.'),
 (.56,.66,.22,.06,'Hidden temple','Roof ridges peek through the trees: the Buddhist retreat of the title, kept small so the mountain dominates.'),
 (.15,.57,.41,.09,'Trees in layered ink','Each tree mixes outline leaves and ink dots in several tones, light first and darker on top.'),
 (.15,.80,.80,.08,'Shore and water','The bottom is left almost empty: plain silk reads as water and mist.'),
 (.73,.23,.12,.05,'Collectors\' seals','Red seals in the corners record later owners, part of the painting\'s history.'),
])
n('cma135431', 'One of a pair with the Tiger, dated to 1269. A dragon emerges from clouds of splashed ink. The pairing follows the old saying "clouds follow the dragon, wind follows the tiger" (雲從龍，風從虎).', [
 (.28,.50,.25,.09,'The dragon\'s head','Whiskers and horns are just a few thin lines; the face appears out of the murk rather than being drawn whole.'),
 (.25,.59,.22,.08,'A claw through the mist','Only fragments of the body show. Your eye fills in the rest, which makes it feel larger.'),
 (.48,.39,.38,.11,'Storm clouds','Broad washes of wet ink, laid over each other, make the clouds. No outlines at all.'),
 (.19,.64,.29,.19,'Gnarled trunk','A dry, broken brush gives the old tree its rough bark, a contrast to the soft clouds.'),
 (.46,.71,.40,.09,'Wind-blown grass','Quick, tapering strokes in one direction show the wind the dragon brings.'),
])
n('cma135432', 'The Tiger, pair to the Dragon. A crouching tiger in wind-blown bamboo, painted with soft, layered ink on silk: Chan (Zen) painting at its most famous, and long treasured in Japan.', [
 (.66,.54,.19,.085,'The face','Round eyes and a broad muzzle, built from many fine strokes rather than a single outline.'),
 (.47,.63,.38,.12,'Fur in layers','Short, pale strokes are laid over grey washes to suggest thick fur. Zoom in to see individual hairs.'),
 (.20,.80,.50,.03,'The tail','A band of dark and light stripes, curving out of the frame.'),
 (.25,.33,.15,.11,'Bare bamboo stem','A thin, dry line at the top: an example of how little Muqi needed to place a setting.'),
 (.40,.60,.50,.14,'Wind in the grass','Grasses sweep across the tiger, painted after the body. This is the "wind follows the tiger" half of the pair.'),
])
n('cma149183', 'A round fan painting of a gibbon swinging from an oak, in the manner of the Southern Song Academy. Gibbons were loved for their cries and seen as creatures of untouched wilderness.', [
 (.27,.26,.19,.39,'Gibbon in wet ink','The body is painted with soft, graded washes and no outline, so it looks furry and light.'),
 (.36,.42,.05,.07,'Pale face','The face is left almost blank inside a dark ring, the classic way to paint a gibbon.'),
 (.62,.17,.14,.63,'Bark and moss','The trunk is drawn with angular strokes and dotted with dark "moss dots" (苔點).'),
 (.32,.16,.25,.17,'Outlined leaves','The oak leaves are outlined and then filled, a more careful technique than the gibbon.'),
 (.50,.62,.24,.23,'Grasses','Long, springy strokes for the grasses and reeds at the base.'),
 (.81,.57,.03,.09,'Tiny signature','Academy painters often hid a small signature along a rock or tree edge.'),
])
n('cma160136', 'A dense, crowded Yuan landscape by Wang Meng, one of the Four Yuan Masters. A scholar sits writing in a thatched house beneath tall pines. Look at how every surface is covered with texture strokes and dots.', [
 (.60,.59,.06,.07,'The scholar at his desk','The tiny seated figure in the pavilion is the subject of the title, writing books under the pines.'),
 (.43,.03,.29,.33,'Pines','Pine needles are drawn as small radiating fans of strokes, layered dark over light.'),
 (.01,.09,.38,.34,'Restless texture','Wang Meng covers his mountains with twisting "ox-hair" strokes and heavy black moss dots, giving them a living, writhing surface.'),
 (.84,.03,.06,.26,'Poem','An inscribed poem at upper right, written into the painting as part of the design.'),
 (.02,.33,.07,.09,'Signature','The artist signs with his studio name, Huanghe Shanqiao 黃鶴山樵, "the woodcutter of Yellow Crane Mountain".'),
 (.79,.83,.18,.09,'Footbridge','A little bridge leads into the scene, inviting the viewer to walk in.'),
])
n('cma149413', 'A fan painting signed by Zhao Mengfu, who revived older styles at the start of the Yuan. Blue-green mountains recall Tang painting, while the pines and fishermen give the scene a quiet, scholarly mood.', [
 (.07,.19,.89,.19,'Blue-green mountains','Mineral blue and green (azurite and malachite) over ink: an archaic style Zhao Mengfu deliberately brought back.'),
 (.51,.31,.35,.51,'Pines','Tall, thin pines with needle clusters drawn as little bursts of strokes.'),
 (.07,.60,.16,.12,'Fishermen','Two small boats with fishermen, the "fisherman\'s joy" of the title.'),
 (.91,.43,.06,.15,'Title and signature','The title 江村漁樂 and the signature 子昂 (Zi\'ang, Zhao Mengfu\'s courtesy name), with his seal.'),
 (.31,.41,.20,.06,'Village life','Tiny houses and figures in the middle distance.'),
])
n('cma136759', 'A crowd of children playing in a garden courtyard: games, masks, parasols and mock officials. "Hundred children" (百子) pictures wished a family many descendants. The theme is associated with the Song painter Su Hanchen.', [
 (.64,.33,.12,.07,'Masks and costumes','Children dress up with masks, playing at theatre or a festival procession.'),
 (.50,.45,.08,.07,'Parasols','Some carry little parasols, part of a mock procession.'),
 (.32,.48,.06,.09,'"Officials" at play','A child in a green robe and hat plays a dignitary, a favourite joke in these scenes.'),
 (.20,.23,.50,.05,'Ruled balustrade','The garden railings are drawn with a ruler-guided line, a technique called jiehua (界畫).'),
 (.78,.10,.17,.32,'Willow and garden rock','A drooping willow frames the corner; the fan shape is filled to its edge.'),
])
n('cma144998', 'An album leaf by Gong Xian, leader of the Eight Masters of Nanjing. A watery village in summer, built almost entirely from rows of ink dabs. It is a good place to study how dots alone can make a landscape.', [
 (.14,.18,.83,.08,'Reeds as rows of dabs','Distant reeds are short vertical marks repeated in rows, each row a little lighter than the one in front.'),
 (.36,.42,.43,.08,'Thatched huts','Small huts with tiny figures, painted with a few light strokes.'),
 (.57,.50,.08,.04,'A boat','A single small boat on open water.'),
 (.12,.56,.45,.35,'Layered ink','Gong Xian builds foliage from many layers of dots, light to dark. He called the method "accumulated ink" (積墨).'),
 (.48,.80,.50,.09,'Bridge and fence','Fine lines for a fence and plank bridge cut across the foreground.'),
 (.05,.59,.04,.05,'Artist\'s seal','A small red seal at left.'),
])
n('cma140154', 'Two birds sit on a twisting pine above a rushing cataract. Painted on silk in the Southern Song Academy manner associated with Li Di.', [
 (.66,.36,.09,.13,'The pair of birds','Two birds side by side, painted with fine outlines and pale colour.'),
 (.13,.21,.39,.34,'Pine needles','Dark clusters of needles, layered over lighter ones.'),
 (.46,.61,.47,.20,'Spray and foam','White foam is left as bare silk between quick grey strokes.'),
 (.13,.58,.28,.20,'Bamboo','Bamboo leaves under the pine in sharper, darker strokes.'),
 (.77,.36,.16,.08,'Crab-claw twigs','Thin branch tips end in hooked "crab-claw" shapes.'),
 (.08,.23,.06,.09,'Collectors\' seals','Seals of later owners.'),
])
n('cma149412', 'A late work by Ni Zan, the most austere of the Four Yuan Masters. A sparse tree, rock and bamboo by a stream, painted in pale, dry ink. Inscriptions by Ni and later admirers fill the top.', [
 (.64,.02,.28,.24,'Ni Zan\'s inscription','The artist\'s own poem and dedication, in his thin, elegant script.'),
 (.03,.02,.60,.24,'Later colophons','Admirers and collectors added poems and seals over the centuries.'),
 (.10,.23,.44,.41,'Tall tree','Dry, light strokes for the branches, with dark dots for leaves.'),
 (.67,.65,.18,.28,'Bamboo','A few stalks of bamboo in pale ink.'),
 (.43,.67,.28,.17,'Rock','The rock is shaped with dry side-brush strokes and very little shading.'),
 (.87,.86,.07,.13,'Seals','Collectors\' seals along the edges.'),
])
n('cma140267', 'A pair of peafowl under bamboo, by Lin Liang, a Ming court painter known for birds in fast, confident ink. The peacock\'s tail is a showcase of wet-ink technique.', [
 (.59,.20,.18,.25,'Tail "eyes"','The eye-spots of the tail feathers are built from circles of wet ink.'),
 (.18,.67,.10,.06,'Peacock\'s head','The male bends low to the ground; small details like the crest are painted quickly.'),
 (.12,.10,.30,.30,'Bamboo','Bamboo leaves in quick, wet, tapering strokes.'),
 (.58,.81,.33,.17,'Rock','Broad side-brush strokes make the rock.'),
 (.03,.09,.07,.06,'Signature','The artist\'s signature, 林良.'),
 (.31,.47,.23,.29,'Body feathers','Layered washes and short strokes for the body and wings.'),
])
n('cma147906', 'Plum blossoms under a full moon, by Wang Mian, the Yuan painter who made ink plum a serious subject. The old trunk and fresh shoots stand for endurance and renewal.', [
 (.11,.21,.17,.10,'The moon','A pale circle washed in lightly, almost invisible.'),
 (.21,.12,.31,.18,'Blossoms in outline','Each flower is drawn as a small ink circle with dots for stamens.'),
 (.35,.72,.63,.26,'Old trunk','Thick, dry strokes with streaks of bare silk, called "flying white" (飛白).'),
 (.02,.56,.19,.10,'Inscription','A poem signed 王元章 (Wang Yuanzhang, Wang Mian\'s courtesy name).'),
 (.76,.65,.22,.15,'New shoots','Long, straight young branches, painted in one movement each.'),
])
n('cma113945', 'A handscroll by Mi Youren, son of Mi Fu. Misty hills float in bands of cloud, painted with wet horizontal dots that later painters called "Mi dots" (米點). Unroll it by zooming and panning left to right.', [
 (.575,.31,.225,.34,'Mi dots','The hills are made of short, horizontal blotches of wet ink placed side by side.'),
 (.50,.56,.47,.17,'Cloud bands','Clouds are left as bare silk between the hills.'),
 (.38,.80,.045,.12,'Winding stream','A thin pale line of water threading into the distance.'),
 (.785,.90,.03,.07,'A boat','A tiny boat on the water at right.'),
 (.35,.05,.07,.57,'Artist\'s inscription','Mi Youren\'s own inscription, signed 元暉 (Yuanhui).'),
 (.035,.10,.16,.83,'Later colophon','A later admirer\'s writing on the mounting paper at the start of the scroll.'),
])
n('cma130497', 'A handscroll by Bada Shanren: rocks, lotus and a few fish on empty paper. The fish swim in water that is never painted. His strange, sideways-glancing fish are among the most recognizable images in Chinese painting.', [
 (.45,.61,.075,.21,'Two fish','A handful of strokes each. The empty paper becomes water.'),
 (.50,.65,.02,.11,'The eye','Bada\'s fish often have a single eye dot placed at the top of the eye circle, giving them a sideways, sceptical look.'),
 (.53,.19,.13,.72,'Balanced rock','A strange rock narrow at the base, drawn mostly in outline.'),
 (.255,.08,.185,.90,'Lotus in splashed ink','Large wet blots for lotus leaves and rocks.'),
 (.665,.11,.06,.42,'Inscriptions','Bada\'s own inscriptions, part of the composition.'),
 (.73,.08,.165,.76,'Overhanging rock','A rock hanging in from the right, with dry dots.'),
])
n('fsgF1909_245c', 'A round fan in the Southern Song Academy style of Ma Yuan: a pavilion on a cliff, with pines and mist. The composition is pushed to one corner, leaving most of the fan empty.', [
 (.42,.04,.15,.14,'Large seal','A collector\'s seal placed at the top of the fan.'),
 (.14,.47,.16,.18,'Pavilion','Figures on a terrace in a richly detailed pavilion.'),
 (.33,.53,.27,.20,'Angular pine','Hooked, angular pine branches, typical of the Ma Yuan manner.'),
 (.60,.26,.35,.26,'Empty space','"One-corner Ma" left whole areas of the composition to mist and distance.'),
 (.23,.63,.20,.26,'Axe-cut strokes','Rocks and cliffs are modelled with broad, sharp-edged "axe-cut" strokes (斧劈皴).'),
 (.77,.76,.12,.06,'Bridge','A small bridge leads out of the scene.'),
])
n('fsgF1911_272', 'Two gibbons play in a tree. Gibbons were a speciality of the Northern Song painter Yi Yuanji, who reportedly studied them in the wild.', [
 (.47,.18,.37,.22,'Reaching gibbon','A long arm stretches across the tree, the black fur painted in dense ink.'),
 (.15,.39,.18,.19,'Clinging gibbon','The second gibbon holds the trunk; note the white ring around its face.'),
 (.49,.43,.33,.11,'Leaves in green','Leaves once brightly green, now darkened with age.'),
 (.90,.67,.06,.11,'Inscription','A small inscription lower right.'),
 (.04,.02,.23,.08,'Seals','Collectors\' seals at the top.'),
])
