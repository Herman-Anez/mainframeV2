# 📝 Formularios: Formik vs React Hook Form

Gestionar formularios en React puede ser complejo: estado, validaciones, errores y rendimiento son factores críticos. **Formik** y **React Hook Form (RHF)** son las dos soluciones líderes, cada una con una filosofía distinta.

---

## 🏗️ Formik: La opción robusta y controlada

Formik sigue el patrón de **componentes controlados**. Cada pulsación de tecla actualiza el estado de React, lo que provoca un re-renderizado del formulario.

*   **Puntos Fuertes**: Excelente documentación, muy predecible, integración nativa con Yup.
*   **Puntos Débiles**: Puede tener problemas de rendimiento en formularios con cientos de campos debido a los re-renders constantes.

```jsx
import { useFormik } from 'formik';
import * as Yup from 'yup';

const SignupForm = () => {
  const formik = useFormik({
    initialValues: { email: '' },
    validationSchema: Yup.object({
      email: Yup.string().email('Invalido').required('Requerido'),
    }),
    onSubmit: values => alert(JSON.stringify(values)),
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <input 
        name="email" 
        onChange={formik.handleChange} 
        value={formik.values.email} 
      />
      {formik.errors.email && <div>{formik.errors.email}</div>}
      <button type="submit">Enviar</button>
    </form>
  );
};
```

---

## ⚡ React Hook Form: Máximo rendimiento

RHF se basa en **componentes no controlados** mediante `refs`. Los inputs no provocan re-renders al escribir, solo cuando se valida o se envía el formulario.

*   **Puntos Fuertes**: Rendimiento imbatible, menos código (boilerplate), validación súper flexible.
*   **Puntos Débiles**: Requiere entender el concepto de `register` y `ref`.

```jsx
import { useForm } from 'react-hook-form';

const SignupForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const onSubmit = data => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email", { required: true })} />
      {errors.email && <span>Este campo es requerido</span>}
      <button type="submit">Enviar</button>
    </form>
  );
};
```

---

## 📊 Comparativa Directa

| Característica | Formik | React Hook Form |
| :--- | :---: | :---: |
| **Enfoque** | Controlado (State) | No Controlado (Refs) |
| **Rendimiento** | ⚠️ Medio | ✅ Alto |
| **Boilerplate** | ⚠️ Alto | ✅ Bajo |
| **Tamaño (Bundle)** | 12.7 kB | 9.1 kB |
| **Validación** | Yup (Integrado) | Zod, Yup, Joi (Resolvers) |

---

## 💡 Recomendación Final

*   **Elige Formik si**: Prefieres una API más explícita, basada en componentes y el rendimiento no es un problema crítico (formularios pequeños/medianos).
*   **Elige React Hook Form si**: Estás construyendo formularios grandes, complejos o complejos, o si buscas la mejor experiencia de desarrollo moderna con **Zod**.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

