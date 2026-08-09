document.addEventListener('DOMContentLoaded', function() {
    
    // --- الجزء الأول: منطق صفحة إضافة أداة ---
    const toolForm = document.getElementById('toolForm');
    if (toolForm) {
        toolForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const name = document.getElementById('toolName').value.trim();
            const category = document.getElementById('toolCategory').value;
            const desc = document.getElementById('toolDesc').value.trim();
            const command = document.getElementById('toolCommand').value.trim();

            if (name === "" || category === "" || desc === "" || command === "") {
                alert("تنبيه: يرجى تعبئة جميع الحقول المطلوبة قبل الحفظ!");
                return;
            }

            const newTool = {
                id: Date.now(),
                name: name,
                category: category,
                desc: desc,
                command: command
            };

            let toolsList = localStorage.getItem('cyberTools');
            toolsList = toolsList === null ? [] : JSON.parse(toolsList);
            
            toolsList.push(newTool);
            localStorage.setItem('cyberTools', JSON.stringify(toolsList));

            alert(`تم حفظ الأداة (${name}) بنجاح!`);
            toolForm.reset();
        });
    }

    // --- الجزء الثاني: منطق صفحة استعراض وعرض الأدوات (DOM Rendering) ---
    const toolsGrid = document.getElementById('toolsGrid');
    if (toolsGrid) {
        // دالة مخصصة لقراءة البيانات وبناء الكروت برمجياً (وظيفة تفاعلية متقدمة)
        function displayTools() {
            toolsGrid.innerHTML = ""; // تنظيف الشبكة أولاً
            
            let toolsList = localStorage.getItem('cyberTools');
            toolsList = toolsList === null ? [] : JSON.parse(toolsList);

            // التحقق إذا كانت المصفوفة فارغة
            if (toolsList.length === 0) {
                toolsGrid.innerHTML = `<p class="no-tools-msg">لا توجد أدوات مسجلة حالياً، قم بالذهاب لصفحة "إضافة أداة" لتسجيل أداتك الأولى.</p>`;
                return;
            }

            // الدوران حول العناصر وبناء كرت لكل أداة (Looping)
            toolsList.forEach(function(tool) {
                const card = document.createElement('div');
                card.classList.add('tool-card'); // تطبيق كلاس الـ CSS

                // تعبئة محتوى الكرت ببيانات الأداة
                card.innerHTML = `
                    <div class="tool-header">
                        <h3>${tool.name}</h3>
                        <span class="tool-badge">${tool.category}</span>
                    </div>
                    <p>${tool.desc}</p>
                    <div class="tool-command-box">$ ${tool.command}</div>
                    <button class="delete-btn" data-id="${tool.id}">حذف الأداة 🗑️</button>
                `;

                toolsGrid.appendChild(card); // إضافة الكرت لصفحة الـ HTML
            });

            // تفعيل أزرار الحذف تفاعلياً
            const deleteButtons = document.querySelectorAll('.delete-btn');
            deleteButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    const idToDelete = Number(button.getAttribute('data-id'));
                    deleteTool(idToDelete);
                });
            });
        }

        // دالة حذف الأداة من الـ LocalStorage وإعادة تحديث الواجهة
        function deleteTool(id) {
            if (confirm("هل أنت متأكد من رغبتك في حذف هذه الأداة من المرجع الموضعي؟")) {
                let toolsList = JSON.parse(localStorage.getItem('cyberTools'));
                
                // تصفية المصفوفة وحذف العنصر المطلوب بناءً على الـ id (Filter Pattern)
                toolsList = toolsList.filter(function(tool) {
                    return tool.id !== id;
                });

                localStorage.setItem('cyberTools', JSON.stringify(toolsList));
                displayTools(); // إعادة رسم الكروت بعد الحذف
            }
        }

        // تشغيل الدالة فور فتح الصفحة ليتم جلب البيانات تلقائياً
        displayTools();
    }
});